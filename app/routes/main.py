from app import app
from flask import render_template, redirect, url_for
from app.services.auth_service import login_required


@app.route("/")
def public_landing():
    """Public Landing Page - loads first for all visitors without gating."""
    return render_template("index.html")


@app.route("/home")
@login_required
def home():
    """Protected Dashboard Home - only accessible to authenticated farmers."""
    return render_template("index.html")


@app.route("/farm-planning")
@login_required
def farm_planning():
    """Protected Farm Planning shortcut."""
    return redirect(url_for("main.home") + "#planning")


@app.route("/crop-recommendation")
@login_required
def crop_recommendation():
    """Protected Crop Recommendation shortcut."""
    return redirect(url_for("main.home") + "#recommendation")


@app.route("/yield-prediction")
@login_required
def yield_prediction():
    """Protected Yield Prediction shortcut."""
    return redirect(url_for("main.home") + "#yield")


@app.route("/smart-advisory")
@login_required
def smart_advisory():
    """Protected Smart Advisory shortcut."""
    return redirect(url_for("main.home") + "#advisory")


@app.route("/about")
@login_required
def about():
    """Protected About page."""
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
