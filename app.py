"""Flask web application for the Plant Tracker."""
import os
import re
from datetime import date

from flask import Flask, flash, redirect, render_template, request, url_for

from load_data import read_dummy_data
from storage import DATA_PATH, load_plants, save_plants
from water_plants import (
    get_plants_needing_water,
    need_water,
    next_watering_date,
)

app = Flask(__name__)
app.secret_key = os.environ.get("PLANT_TRACKER_SECRET", "plant-tracker-dev-secret")

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _find_plant(plant_list, name):
    """Return the first plant in plant_list whose name matches (case-insensitive)."""
    for plant in plant_list:
        if plant["name"].lower() == name.lower():
            return plant
    return None


def _persist(plant_list, success_message):
    """Save plant_list; flash success or a writable-data error. Returns True if saved."""
    if save_plants(plant_list):
        flash(success_message, "success")
        return True
    flash(
        "Could not save plant data. Ensure the data directory is writable by the web server "
        f"(see {DATA_PATH}).",
        "error",
    )
    return False


def _decorate(plant_list):
    """Return plants annotated with next_watering and needs_water for templates."""
    decorated = []
    for plant in plant_list:
        next_date = next_watering_date(plant)
        decorated.append({
            **plant,
            "next_watering": str(next_date) if next_date else "N/A",
            "needs_water": need_water(plant),
        })
    return decorated


@app.route("/")
def index():
    """List plants with optional filtering by name, location, or watering need."""
    plant_list = load_plants()
    filter_by = request.args.get("filter", "all")
    query = request.args.get("q", "").strip()

    if filter_by == "name" and query:
        filtered = [p for p in plant_list if p["name"].lower() == query.lower()]
    elif filter_by == "location" and query:
        filtered = [p for p in plant_list if p["location"].lower() == query.lower()]
    elif filter_by == "needs_water":
        filtered = get_plants_needing_water(plant_list)
    else:
        filtered = plant_list

    return render_template(
        "index.html",
        plants=_decorate(filtered),
        total=len(plant_list),
        needing_water=len(get_plants_needing_water(plant_list)),
        filter_by=filter_by,
        query=query,
    )


@app.route("/add", methods=["GET", "POST"])
def add():
    """Create a new plant from form input."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        location = request.form.get("location", "").strip()
        last_watered = request.form.get("last_watered", "").strip()
        interval_raw = request.form.get("water_interval_days", "").strip()

        plant_list = load_plants()
        errors = []

        if not name:
            errors.append("Name is required.")
        elif _find_plant(plant_list, name):
            errors.append(f"A plant named '{name}' already exists.")
        if not location:
            errors.append("Location is required.")
        if not DATE_RE.match(last_watered):
            errors.append("Last watered must be in YYYY-MM-DD format.")
        if not interval_raw.isdigit() or int(interval_raw) <= 0:
            errors.append("Water interval must be a positive whole number.")

        if errors:
            for e in errors:
                flash(e, "error")
            return render_template(
                "add.html",
                form={
                    "name": name,
                    "location": location,
                    "last_watered": last_watered,
                    "water_interval_days": interval_raw,
                },
            )

        plant_list.append({
            "name": name,
            "location": location,
            "last_watered": last_watered,
            "water_interval_days": int(interval_raw),
        })
        if not _persist(plant_list, f"Plant '{name}' added successfully."):
            return render_template(
                "add.html",
                form={
                    "name": name,
                    "location": location,
                    "last_watered": last_watered,
                    "water_interval_days": interval_raw,
                },
            )
        return redirect(url_for("index"))

    return render_template("add.html", form={})


@app.route("/edit/<name>", methods=["GET", "POST"])
def edit(name):
    """Edit an existing plant identified by name."""
    plant_list = load_plants()
    plant = _find_plant(plant_list, name)
    if plant is None:
        flash(f"No plant named '{name}' found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        new_name = request.form.get("name", "").strip()
        new_location = request.form.get("location", "").strip()
        new_last_watered = request.form.get("last_watered", "").strip()
        new_interval_raw = request.form.get("water_interval_days", "").strip()

        errors = []
        if not new_name:
            errors.append("Name is required.")
        else:
            duplicate = _find_plant(plant_list, new_name)
            if duplicate is not None and duplicate is not plant:
                errors.append(f"A plant named '{new_name}' already exists.")
        if not new_location:
            errors.append("Location is required.")
        if not DATE_RE.match(new_last_watered):
            errors.append("Last watered must be in YYYY-MM-DD format.")
        if not new_interval_raw.isdigit() or int(new_interval_raw) <= 0:
            errors.append("Water interval must be a positive whole number.")

        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("edit.html", plant={
                "name": new_name,
                "location": new_location,
                "last_watered": new_last_watered,
                "water_interval_days": new_interval_raw,
            }, original_name=plant["name"])

        plant["name"] = new_name
        plant["location"] = new_location
        plant["last_watered"] = new_last_watered
        plant["water_interval_days"] = int(new_interval_raw)
        if not _persist(plant_list, f"Plant '{new_name}' updated."):
            return render_template("edit.html", plant={
                "name": new_name,
                "location": new_location,
                "last_watered": new_last_watered,
                "water_interval_days": new_interval_raw,
            }, original_name=plant["name"])
        return redirect(url_for("index"))

    return render_template("edit.html", plant=plant, original_name=plant["name"])


@app.route("/delete/<name>", methods=["POST"])
def delete(name):
    """Remove a plant by name."""
    plant_list = load_plants()
    plant = _find_plant(plant_list, name)
    if plant is None:
        flash(f"No plant named '{name}' found.", "error")
    else:
        plant_list.remove(plant)
        _persist(plant_list, f"Plant '{name}' removed.")
    return redirect(url_for("index"))


@app.route("/water/<name>", methods=["POST"])
def water_one(name):
    """Mark a single plant as watered today."""
    plant_list = load_plants()
    plant = _find_plant(plant_list, name)
    if plant is None:
        flash(f"No plant named '{name}' found.", "error")
    else:
        plant["last_watered"] = str(date.today())
        _persist(plant_list, f"'{name}' watered today.")
    return redirect(request.referrer or url_for("index"))


@app.route("/water-needing", methods=["POST"])
def water_needing():
    """Mark all plants that currently need water as watered today."""
    plant_list = load_plants()
    today = str(date.today())
    needing = get_plants_needing_water(plant_list)
    for plant in needing:
        plant["last_watered"] = today
    _persist(plant_list, f"Watered {len(needing)} plant(s) that needed water.")
    return redirect(url_for("index"))


@app.route("/water-location", methods=["POST"])
def water_location():
    """Mark all plants at a given location that need water as watered today."""
    location = request.form.get("location", "").strip()
    if not location:
        flash("Please provide a location.", "error")
        return redirect(url_for("index"))

    plant_list = load_plants()
    today = str(date.today())
    needing = get_plants_needing_water(plant_list, location=location)
    for plant in needing:
        plant["last_watered"] = today
    if needing:
        _persist(plant_list, f"Watered {len(needing)} plant(s) at '{location}'.")
    else:
        flash(f"No plants at '{location}' need water right now.", "info")
    return redirect(url_for("index"))


@app.route("/load-dummy", methods=["POST"])
def load_dummy():
    """Load plants from the bundled CSV in replace or append mode."""
    mode = request.form.get("mode", "append")
    new_plants = read_dummy_data()

    if mode == "replace":
        _persist(new_plants, f"Loaded {len(new_plants)} plant(s) from dummy data (replaced existing).")
        return redirect(url_for("index"))

    plant_list = load_plants()
    existing_names = {p["name"].lower() for p in plant_list}
    added = 0
    skipped = 0
    for plant in new_plants:
        if plant["name"].lower() in existing_names:
            skipped += 1
        else:
            plant_list.append(plant)
            existing_names.add(plant["name"].lower())
            added += 1
    _persist(plant_list, f"Loaded {added} plant(s) from dummy data; skipped {skipped} duplicate(s).")
    return redirect(url_for("index"))


@app.route("/summary")
def summary():
    """Show an overview of the plant collection."""
    plant_list = load_plants()
    needing = get_plants_needing_water(plant_list)
    return render_template(
        "summary.html",
        total=len(plant_list),
        needing=_decorate(needing),
        plants=_decorate(plant_list),
    )


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
