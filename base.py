from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__, static_folder="static", static_url_path="/static")

@app.route('/')
def welcome():

    return render_template('welcome.html')


@app.route('/option', methods=['GET', 'POST'])
def process_option():

    selected_option = None

    if request.method == 'POST':
        selected_option = request.form.get('choice')


    if selected_option == "option1":
        return redirect(url_for('option1'))
    elif selected_option == "option2":
        return redirect(url_for('option2'))
    elif selected_option == "option3":
        return redirect(url_for('option3'))
    elif selected_option == "option4":
        return redirect(url_for('option4'))
    elif selected_option == "option5":
        return redirect(url_for('option5'))

    if selected_option is None:
        return "Invalid option or method used."

@app.route('/option1')
def option1():

    return render_template('option1.html')


    
if __name__ == '__main__':
    app.run(debug=True)
    



