# Step 1: Grab a pre-built, lightweiht image of python 3.11
FROM python:3.11-slim 

# Step 2: Create a secure operational directory inside the container
WORKDIR /app

#Step 3: Copy your dependecies list into the box
COPY requirements.txt .

# Step 4: Run the installer inside the box to secure your packages
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy all of your local source files into the container
COPY . .

# Step 6: Expose Port 5000 so the container can hear outside network traffic
EXPOSE 5000

# Step 7: Automatically fire up the backend server on boot
CMD ["python", "app.py"]