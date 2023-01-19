from .routes import *

app = create_app()
create_routes(app)
app.run(debug=True, host="0.0.0.0")