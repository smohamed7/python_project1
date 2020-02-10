from flask import Flask,render_template
import pygal
import psycopg2

app = Flask(__name__)


@app.route('/<sule>')
def hello_world(sule):
    return '<h1>Hello sule</h1>'.format(sule)

@app.route('/about')
def about():
     return render_template('about.html',title='my about page')

@app.route("/contact")
def contact():
    return render_template('contacts.html')

@app.route("/services")
def services():
    return render_template('services.html')

@app.route("/person/<name>/<int:age>")
def person(name,age):
    return "<h1> {} is {} years old </h1>".format(name,age)

@app.route("/add/<int:numb1>/<int:numb2>")
def add(numb1,numb2):
    total=numb1+numb2
    return str(total)

@app.route("/index")
def index():

    data=[('internet explorer',19.5),('chrome',36.3),('Opera', 2.3),('Safari', 4.5)]

    pie_chart = pygal.Pie()
    pie_chart.title = 'Browser usage in February 2012 (in %)'
    pie_chart.add(data[0][0],data[0][1])
    pie_chart.add(data[1][0],data[1][1])
    pie_chart.add(data[2][0],data[2][1])
    pie_chart.add(data[3][0],data[3][1])

    pie_data=pie_chart.render_data_uri()

@app.route('/line')
def line():
    conn=psycopg2.connect("dbname = sales_demo user=postgres host =localhost password=123")
    cur=conn.cursor()
    cur.execute("""SELECT (EXTRACT (MONTH FROM sales.created_at)as months,
      SUM(sales.quantity)as total sales
      FROM public.sales
      GROUP BY months
      ORDER BY months
      """)
    records = cur.fetchall()

    line_chart=pygal.Line()
    line_chart.title="sales for 2019"
    x=[]
    y=[]
    for i in records:
        x.append(i[0])
        y.append(i[1])

    line_chart.x_labels=map(str,x)
    line_chart.add("sales",y)

    line_chart=line_chart.render_data_uri()
    return render_template('index.html',line_chart=line_chart)




if __name__ == '__main__':
    app.run()
