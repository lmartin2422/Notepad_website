from website import create_app  # grabs the create_app function from the init file within the website folder

app = create_app()

if __name__ == '__main__':  # allows you to run an app/website from a server
    app.run(debug=True)