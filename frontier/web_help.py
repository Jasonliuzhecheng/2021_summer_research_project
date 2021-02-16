from flask import render_template, request, flash


def get_fields(fields):
	result = dict()
	for field in fields:
		if field == "dataset": result[field] = request.form.getlist(field)
		elif field == "group":
			data = request.form.get(field)
			result[field] = tuple(float(i) for i in data.split(" ")) if len(data) != 0 else tuple()
		else: result[field] = request.form.get(field)
	return result


def demo_main(fields, demo_html, plot_html, query_func, title, x_label=None):
	if request.method == "POST":
		fields = get_fields(fields)
		for field in fields:
			if not isinstance(fields[field], tuple) and not fields[field]:
				flash("Expected parameters {} missing".format(field))
		else:
			data = query_func(**fields)
			if x_label is None:
				return render_template(plot_html, data = data, title = title)
			else:
				return render_template(plot_html, data = data, title = title, x_label = x_label)

	return render_template(demo_html)
