## Postman Collection

To test the API endpoints, you can use the Postman collection provided.

1. Download and install Postman from [here](https://www.postman.com/downloads/).
2. Download the Postman collection JSON file from(https://www.postman.com/orbital-module-geologist-51477300/workspace/movie/).
3. Open Postman and import the collection:
   - Click on "Import" in the top-left corner.
   - Choose the downloaded JSON file.
4. Follow the steps in the collection to test each endpoint.

### API Endpoints

- **Register**: `POST /api/auth/register/`
- **Login**: `POST /api/auth/login/`
- **Fetch Movies**: `GET /movies/`
- **Create Review**: `POST /reviews/`
- **Read Reviews**: `GET /reviews/`
- **Update Review**: `PUT /reviews/<review-id>/`
- **Delete Review**: `DELETE /reviews/<review-id>/`
- **Fetch Recommendations**: `GET /api/recommendations/`


1. Clone the repository:

   ```bash
   git clone https://github.com/shivamjai17/Movie-Recomdatiom-API
   cd movie_review_api
   python -m venv myenv
   cd myenv
   scripts/activate (Windows)
   source bin/activate (MacOS/Linux)
   cd ..
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver





