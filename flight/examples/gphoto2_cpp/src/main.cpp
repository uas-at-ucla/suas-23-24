#include <boost/interprocess/mapped_region.hpp>
#include <boost/interprocess/shared_memory_object.hpp>
#include <chrono>
#include <ctime>
#include <curl/curl.h>
#include <fcntl.h>
#include <fstream>
#include <gphoto2/gphoto2-camera.h>
#include <iostream>

// This function takes an image from a usb-connected camera and stores it to a
// data array variable
static void capture_to_memory(const char **picture_data,
                              unsigned long *picture_size) {
  // Create a camera object and context
  Camera *camera;
  GPContext *context = gp_context_new();
  gp_camera_new(&camera);
  gp_camera_init(camera, context);

  // Create the camera file and take an image on the camera, saving it to memory
  // on the camera
  CameraFile *file;
  CameraFilePath camera_file_path;
  std::cout << "Capturing image" << std::endl;
  gp_camera_capture(camera, GP_CAPTURE_IMAGE, &camera_file_path, context);

  printf("Pathname on camera: %s/%s\n", camera_file_path.folder,
         camera_file_path.name);

  // Create a new local variable and copy its data from the camera to the local
  // memory variable
  gp_file_new(&file);
  gp_camera_file_get(camera, camera_file_path.folder, camera_file_path.name,
                     GP_FILE_TYPE_NORMAL, file, context);
  gp_file_get_data_and_size(file, picture_data, picture_size);
  std::cout << "Image saved into memory variable" << std::endl;

  // Delete the file on the camera to free up space
  gp_camera_file_delete(camera, camera_file_path.folder, camera_file_path.name,
                        context);
  std::cout << "Deleted on camera" << std::endl;
}

// This function takes in the data array, size, and desired shared memory object
// name and puts a shared memory object into /dev/shm
static void send_to_shared_mem(const char *picture_data,
                               unsigned long *picture_size,
                               std::string shared_mem_name) {
  try {
    // Create shared memory object with the given name and with read_write
    // permissions
    boost::interprocess::shared_memory_object shm(
        boost::interprocess::open_or_create, shared_mem_name.c_str(),
        boost::interprocess::read_write);
    shm.truncate(*picture_size);

    // Memory map the object
    boost::interprocess::mapped_region region(shm,
                                              boost::interprocess::read_write);

    // Copy image data to the object and report success
    void *addr = region.get_address();
    std::memcpy(addr, picture_data, *picture_size);
    std::cout << "Image data sent to shared memory object." << std::endl;

  } catch (const std::exception &e) {
    // Print error if there is any
    std::cerr << e.what() << std::endl;
  }
}

// This function posts an http request containing the shared memory name and
// telemetry data to be picked up by the Python server
static void post_request(std::string shared_mem_name) {
  // Make curl object
  CURL *curl;
  CURLcode request;

  // Intialize curl
  curl_global_init(CURL_GLOBAL_DEFAULT);
  curl = curl_easy_init();

  if (curl) {
    // Set url to make post to
    curl_easy_setopt(curl, CURLOPT_URL, "http://localhost:8003/odlc");

    // Set request to be a POST
    curl_easy_setopt(curl, CURLOPT_POST, 1L);

    // Set JSON data to send the name of the shared memory object and the
    // telemetry data taken at the same time
    std::string json_string = "";
    json_string += "{\"img_name\": \"" + shared_mem_name +
                   "\", \"altitude\": 0, \"latitude\": 0, \"longitude\": 0, "
                   "\"heading\": 0}";
    const char *json_data = json_string.c_str();
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, json_data);

    // Set content type header to json
    struct curl_slist *headers = nullptr;
    headers = curl_slist_append(headers, "Content-Type: application/json");
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

    // Send the request
    request = curl_easy_perform(curl);

    // Output if the request was successful or failed
    if (request != CURLE_OK) {
      std::cerr << "Request failed: " << curl_easy_strerror(request)
                << std::endl;
    } else {
      std::cout << "Request success." << std::endl;
    }

    // Clean up
    curl_easy_cleanup(curl);
    curl_slist_free_all(headers);
  }

  curl_global_cleanup();
}

int main(int argc, char *argv[]) {
  // Gets the current time of system and saves it to a string "time_info"
  time_t raw_time;
  struct tm *time_info;
  char timestamp[80];
  time(&raw_time);
  time_info = localtime(&raw_time);
  strftime(timestamp, sizeof(timestamp), "%m-%d_%H%M%S", time_info);

  std::string shared_mem_name;

  // Try to set the memory name to the first argument provided when running
  // binary, if none provided then use the current time of the system.
  try {
    std::string temp_name(argv[1]);
    shared_mem_name = temp_name;
  } catch (const std::exception &e) {
    shared_mem_name = timestamp;
  }

  // Create two variables to hold the data and size of data of picture then take
  // a photo and save respective data to its variables using the function call
  char *picture_data;
  unsigned long picture_size;
  capture_to_memory((const char **)&picture_data, &picture_size);

  // Read the binary and store it in a picture file
  std::string file_type = ".cr2";
  std::ofstream outputFile(timestamp + file_type, std::ios::binary);
  if (outputFile.is_open()) {
    outputFile.write(picture_data, picture_size);
    outputFile.close();
    std::cout << "Data written as " << timestamp << file_type << std::endl;
  }

  // Send the data to shared memory folder /dev/shm and post an http request for
  // the Python server to pick up with the shared memory name.
  send_to_shared_mem(picture_data, &picture_size, shared_mem_name);
  post_request(shared_mem_name);
}
