# Placeholder Image Server

This is a simple Django project that serves placeholder images of custom sizes. It allows you to generate placeholder images on the fly using a custom Django view.

## How to Use

1. Clone this repository to your local machine.

2. Make sure you have Python and Django installed.

3. Install the required Python packages using pip:
    pip install -r requirements.txt 

4. Start the gunicorn server:
    gunicorn main --log-file=- 

5. Open your web browser and visit the following URL to generate a placeholder image:
    http://localhost:8000/image/<width>x<height>/
    Note : Replace `<width>` and `<height>` with the desired dimensions of the placeholder image.

6. The generated placeholder image will be displayed in your web browser.

## Dependencies
-Python 3.11.4+
- Django 4.2.4+
- gunicorn 21.2.0+
- Pillow 10.0.0+ (Python Imaging Library)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.