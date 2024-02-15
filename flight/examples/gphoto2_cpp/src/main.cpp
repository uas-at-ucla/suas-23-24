#include <boost/interprocess/mapped_region.hpp>
#include <boost/interprocess/shared_memory_object.hpp>
#include <chrono>
#include <ctime>
#include <curl/curl.h>
#include <fcntl.h>
#include <fstream>
#include <gphoto2/gphoto2-camera.h>
#include <iostream>

static void canon_enable_capture(Camera *camera, GPContext *context) {
  // Set the camera port (you may need to adjust this based on your camera
  // model)
  CameraWidget *rootWidget;
  gp_camera_get_config(camera, &rootWidget, context);

  // Find the capture mode widget
  CameraWidget *captureModeWidget;
  gp_widget_get_child_by_name(rootWidget, "capturemode", &captureModeWidget);

  if (captureModeWidget) {
    // Set the capture mode to "1" (assuming "1" represents continuous shooting
    // mode)
    gp_widget_set_value(captureModeWidget, "1");

    // Apply the changes to the camera
    gp_camera_set_config(camera, rootWidget, context);

    std::cout << "Capture mode set successfully." << std::endl;
  } else {
    std::cerr << "Unable to find capture mode widget." << std::endl;
  }

  // Free the camera context
  gp_widget_free(rootWidget);
  gp_camera_free(camera);
}

static void capture_to_memory(const char **picture_data,
                              unsigned long *picture_size) {
  Camera *camera;
  GPContext *context = gp_context_new();
  gp_camera_new(&camera);
  gp_camera_init(camera, context);

  CameraFile *file;
  CameraFilePath camera_file_path;
  std::cout << "Capturing image" << std::endl;
  gp_camera_capture(camera, GP_CAPTURE_IMAGE, &camera_file_path, context);

  printf("Pathname on camera: %s/%s\n", camera_file_path.folder,
         camera_file_path.name);

  gp_file_new(&file);
  gp_camera_file_get(camera, camera_file_path.folder, camera_file_path.name,
                     GP_FILE_TYPE_NORMAL, file, context);
  gp_file_get_data_and_size(file, picture_data, picture_size);
  std::cout << "Image saved into memory variable" << std::endl;
  gp_camera_file_delete(camera, camera_file_path.folder, camera_file_path.name,
                        context);
  std::cout << "Deleted on camera" << std::endl;
}

static void send_to_shared_mem(const char *picture_data,
                               unsigned long *picture_size,
                               std::string shared_mem_name) {
  try {
    // Create shared memory object
    boost::interprocess::shared_memory_object shm(
        boost::interprocess::open_or_create, shared_mem_name.c_str(),
        boost::interprocess::read_write);
    shm.truncate(*picture_size);

    // Memory map the object
    boost::interprocess::mapped_region region(shm,
                                              boost::interprocess::read_write);
    // Copy the image data to the object
    void *addr = region.get_address();
    std::memcpy(addr, picture_data, *picture_size);
    std::cout << "Image data sent to shared memory object." << std::endl;

  } catch (const std::exception &e) {
    // Print error if there is any
    std::cerr << e.what() << std::endl;
  }
}

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

    // Set JSON data to send
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
  time_t raw_time;
  struct tm *time_info;
  char timestamp[80];
  time(&raw_time);
  time_info = localtime(&raw_time);
  strftime(timestamp, sizeof(timestamp), "%m-%d_%H%M%S", time_info);
  std::string shared_mem_name;

  try {
    std::string temp_name(argv[1]);
    shared_mem_name = temp_name;
  } catch (const std::exception &e) {
    std::cerr << e.what() << std::endl;
    shared_mem_name = timestamp;
  }

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
  send_to_shared_mem(picture_data, &picture_size, shared_mem_name);
  post_request(shared_mem_name);
}
