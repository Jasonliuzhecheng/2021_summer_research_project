from process import *
from flask import Flask, render_template
from frontier.web_help import demo_main

app = Flask(__name__)
app.secret_key = "Glucose"


# link to main page
@app.route("/glucose_analyst")
def home():
    return render_template("home.html")


# link to main page
@app.route("/glucose_analyst/about")
def about():
    return render_template("about.html")


# link to demo
@app.route("/glucose_analyst/demo")
def demo():
    return render_template("demo/demo.html")


# link to average_glucose
@app.route("/glucose_analyst/demo/average_glucose", methods = ["GET", "POST"])
def average_glucose():
    return demo_main(fields = ['dataset', 'interval', 'cycle'],
                     demo_html = "demo/average_glucose.html", plot_html = "tools/plot.html",
                     query_func = get_time_vs_gl, title = "Average glucose for all groups")


# link to average_glucose_exercise_status
@app.route("/glucose_analyst/demo/average_glucose_exercise_status", methods = ["GET", "POST"])
def average_glucose_exercise_status():
    return demo_main(fields = ['dataset', 'exercise_status', 'interval', 'cycle'], query_func = get_time_vs_exercise_gl,
                     demo_html = "demo/average_glucose_exercise_status.html", plot_html = "tools/plot.html",
                     title = "Average glucose based on exercise status")


# link to average_glucose_insulin
@app.route("/glucose_analyst/demo/average_glucose_insulin", methods = ["GET", "POST"])
def average_glucose_insulin():
    return demo_main(fields = ['dataset', 'interval', 'max_duration'], query_func = get_insulin_time_vs_gl,
                     demo_html = "demo/average_glucose_insulin.html", plot_html = "tools/plot.html",
                     title = "Average glucose after inject insulin")


# link to average_glucose_meal
@app.route("/glucose_analyst/demo/average_glucose_meal", methods = ["GET", "POST"])
def average_glucose_meal():
    return demo_main(fields = ['dataset', 'interval', 'max_duration'], query_func = get_meal_vs_gl,
                     demo_html = "demo/average_glucose_meal.html", plot_html = "tools/plot.html",
                     title = "Average glucose after have meal")


# link to average_glucose_snack
@app.route("/glucose_analyst/demo/average_glucose_snack", methods = ["GET", "POST"])
def average_glucose_snack():
    return demo_main(fields = ['dataset', 'interval', 'max_duration'], query_func = get_snack_vs_gl,
                     demo_html = "demo/average_glucose_snack.html", plot_html = "tools/plot.html",
                     title = "Average glucose after have snack")


# link to average_glucose_exercise
@app.route("/glucose_analyst/demo/average_glucose_exercise", methods = ["GET", "POST"])
def average_glucose_exercise():
    return demo_main(fields = ['dataset', 'interval', 'max_duration'], query_func = get_exercise_vs_gl,
                     demo_html = "demo/average_glucose_exercise.html", plot_html = "tools/plot.html",
                     title = "Average glucose after have exercise")


# link to average_glucose_fast_insulin
@app.route("/glucose_analyst/demo/average_glucose_fast_insulin", methods = ["GET", "POST"])
def average_glucose_fast_insulin():
    return demo_main(fields = ['dataset', 'interval', 'max_duration'], query_func = get_fast_insulin_time_vs_gl,
                     demo_html = "demo/average_glucose_fast_insulin.html", plot_html = "tools/plot.html",
                     title = "Average glucose after have fast insulin")


# link to average_glucose_strict_meal
@app.route("/glucose_analyst/demo/average_glucose_strict_meal", methods = ["GET", "POST"])
def average_glucose_strict_meal():
    return demo_main(fields = ['dataset', 'group', 'interval', 'cycle'], query_func = get_strict_meal_vs_gl,
                     demo_html = "demo/average_glucose_strict_meal.html", plot_html = "tools/multi_plot.html",
                     title = "strict meal level vs average glucose")


# link to average_glucose_pre_meal
@app.route("/glucose_analyst/demo/average_glucose_pre_meal", methods = ["GET", "POST"])
def average_glucose_pre_meal():
    return demo_main(fields = ['dataset', 'group', 'interval', 'cycle'], query_func = get_pre_meal_vs_gl,
                     demo_html = "demo/average_glucose_pre_meal.html", plot_html = "tools/multi_plot.html",
                     title = "pre meal level vs average glucose")


# link to average_glucose_trouble_sleep
@app.route("/glucose_analyst/demo/average_glucose_trouble_sleep", methods = ["GET", "POST"])
def average_glucose_trouble_sleep():
    return demo_main(fields = ['dataset', 'group', 'interval', 'cycle'], query_func = get_trouble_sleep_vs_gl,
                     demo_html = "demo/average_glucose_trouble_sleep.html", plot_html = "tools/multi_plot.html",
                     title = "trouble sleep level vs average glucose")


# link to average_glucose_weight
@app.route("/glucose_analyst/demo/average_glucose_weight", methods = ["GET", "POST"])
def average_glucose_weight():
    return demo_main(fields = ['dataset', 'group', 'interval', 'cycle'], query_func = get_weight_vs_gl,
                     demo_html = "demo/average_glucose_weight.html", plot_html = "tools/multi_plot.html",
                     title = "weight level vs average glucose")


# link to average_glucose_insulin_method
@app.route("/glucose_analyst/demo/average_glucose_insulin_method", methods = ["GET", "POST"])
def average_glucose_insulin_method():
    return demo_main(fields = ['dataset', 'interval', 'cycle'], query_func = get_insulin_method_vs_gl,
                     demo_html = "demo/average_glucose_insulin_method.html", plot_html = "tools/multi_plot.html",
                     title = "insulin method level vs average glucose")


# link to average_ins_weight
@app.route("/glucose_analyst/demo/average_ins_weight", methods = ["GET", "POST"])
def average_ins_weight():
    return demo_main(fields = ['dataset', 'group'], query_func = get_weight_vs_daily_insulin,
                     demo_html = "demo/average_ins_weight.html", plot_html = "tools/histogram.html",
                     title = 'Daily insulin over different weight groups', x_label='daily insulin(units)')


# link to gender_statistic
@app.route("/glucose_analyst/demo/gender_statistic", methods = ["GET", "POST"])
def gender_statistic():
    return demo_main(fields = ['dataset'], query_func = get_gender,
                     demo_html = "demo/gender_statistic.html", plot_html = "tools/pie.html",
                     title = 'gender statistic', x_label = 'gender')


# link to race_statistic
@app.route("/glucose_analyst/demo/race_statistic", methods = ["GET", "POST"])
def race_statistic():
    return demo_main(fields = ['dataset'], query_func = get_race,
                     demo_html = "demo/race_statistic.html", plot_html = "tools/pie.html",
                     title = 'race statistic', x_label = 'race')


# link to diagnostic_age_statistic
@app.route("/glucose_analyst/demo/diagnostic_age_statistic", methods = ["GET", "POST"])
def diagnostic_age_statistic():
    return demo_main(fields = ['dataset', 'group'], query_func = get_diag_age,
                     demo_html = "demo/diagnostic_age_statistic.html", plot_html = "tools/pie.html",
                     title = 'diagnostic age statistic', x_label = 'diagnostic age')


# link to low_glucose_statistic
@app.route("/glucose_analyst/demo/low_glucose_statistic", methods = ["GET", "POST"])
def low_glucose_statistic():
    return demo_main(fields = ['dataset'], query_func = get_low_gl,
                     demo_html = "demo/low_glucose_statistic.html", plot_html = "tools/pie.html",
                     title = 'low glucose statistic', x_label = 'low glucose')


# link to systolic_blood_pressure_statistic
@app.route("/glucose_analyst/demo/systolic_blood_pressure_statistic", methods = ["GET", "POST"])
def systolic_blood_pressure_statistic():
    return demo_main(fields = ['dataset', 'group'], query_func = get_bld_pr_sys,
                     demo_html = "demo/systolic_blood_pressure_statistic.html", plot_html = "tools/pie.html",
                     title = 'systolic blood pressure statistic', x_label = 'systolic blood pressure')


# link to diastolic_blood_pressure_statistic
@app.route("/glucose_analyst/demo/diastolic_blood_pressure_statistic", methods = ["GET", "POST"])
def diastolic_blood_pressure_statistic():
    return demo_main(fields = ['dataset', 'group'], query_func = get_bld_pr_dia,
                     demo_html = "demo/diastolic_blood_pressure_statistic.html", plot_html = "tools/pie.html",
                     title = 'diastolic blood pressure statistic', x_label = 'diastolic blood pressure')


# link to weight_statistic
@app.route("/glucose_analyst/demo/weight_statistic", methods = ["GET", "POST"])
def weight_statistic():
    return demo_main(fields = ['dataset', 'group'], query_func = get_weight,
                     demo_html = "demo/weight_statistic.html", plot_html = "tools/pie.html",
                     title = 'weight statistic', x_label = 'weight')


# link to daily_insulin_statistic
@app.route("/glucose_analyst/demo/daily_insulin_statistic", methods = ["GET", "POST"])
def daily_insulin_statistic():
    return demo_main(fields = ['dataset', 'group'], query_func = get_daily_insulin,
                     demo_html = "demo/daily_insulin_statistic.html", plot_html = "tools/pie.html",
                     title = 'daily insulin statistic', x_label = 'daily insulin')


# link to breakfast_ratio_statistic
@app.route("/glucose_analyst/demo/breakfast_ratio_statistic", methods = ["GET", "POST"])
def breakfast_ratio_statistic():
    return demo_main(fields = ['dataset', 'group'], query_func = get_breakfast_ratio,
                     demo_html = "demo/breakfast_ratio_statistic.html", plot_html = "tools/pie.html",
                     title = 'breakfast ratio statistic', x_label = 'breakfast ratio')


# link to lunch_ratio_statistic
@app.route("/glucose_analyst/demo/lunch_ratio_statistic", methods = ["GET", "POST"])
def lunch_ratio_statistic():
    return demo_main(fields = ['dataset', 'group'], query_func = get_lunch_ratio,
                     demo_html = "demo/lunch_ratio_statistic.html", plot_html = "tools/pie.html",
                     title = 'lunch ratio statistic', x_label = 'lunch ratio')


# link to dinner_ratio_statistic
@app.route("/glucose_analyst/demo/dinner_ratio_statistic", methods = ["GET", "POST"])
def dinner_ratio_statistic():
    return demo_main(fields = ['dataset', 'group'], query_func = get_dinner_ratio,
                     demo_html = "demo/dinner_ratio_statistic.html", plot_html = "tools/pie.html",
                     title = 'dinner ratio statistic', x_label = 'dinner ratio')


if __name__ == '__main__':
    app.run(debug=True)
