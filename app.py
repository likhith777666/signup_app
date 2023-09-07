from flask import Flask, render_template, request
from jinja2 import Environment, FileSystemLoader

from flask_mysqldb import MySQL
import yaml

app = Flask(__name__, template_folder=r'C:\Users\asus\OneDrive\Desktop\assignmentprj\template')




# Assuming your YAML file is named 'db.yaml' in the same directory
yaml_file_path = 'db.yaml'

try:
    with open(yaml_file_path, 'r') as yaml_file:
        db_config = yaml.load(yaml_file, Loader=yaml.FullLoader)

    # Now 'db_config' contains the parsed YAML data
    # You can access values like db_config['key']

except FileNotFoundError:
    print(f"YAML file '{yaml_file_path}' not found.")
except Exception as e:
    print(f"An error occurred while reading the YAML file: {str(e)}")

app.config['MYSQL_HOST']=db_config['mysql_host']
app.config['MYSQL_USER']=db_config['mysql_user']
app.config['MYSQL_PASSWORD']=db_config['mysql_password']
app.config['MYSQL_DB']=db_config['mysql_db']

mysql=MySQL(app)


@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
       userDetails=request.form
       name=userDetails['name']
       email=userDetails['email']
       cur = mysql.connection.cursor()
       cur.execute("INSERT INTO user (password, email) VALUES (%s, %s)", (name, email))

       mysql.connection.commit()
       cur.close()
       return 'success'
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)