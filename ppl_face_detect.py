# Save this file to your Github as OpenCV-13-FaceRec1.py
import cv2
import face_recognition
import numpy as np
import dlib

video_capture = cv2.VideoCapture(0)

# Load and find the known images location and encode the face
img_CWY = face_recognition.load_image_file(r'C:\Users\250498705\PycharmProjects\Project1\Resources\CWY.jpg')
img_CWY = cv2.cvtColor(img_CWY, cv2.COLOR_RGB2BGR)
faceLoc_CWY = face_recognition.face_locations(img_CWY)[0]
encode_CWY = face_recognition.face_encodings(img_CWY)[0]
cv2.rectangle(img_CWY, (faceLoc_CWY[3], faceLoc_CWY[0]), (faceLoc_CWY[1], faceLoc_CWY[2]), (255, 0, 255), 2)

print("1")

# Load and find unknown images, encode, and compare to known faces
img_Xavier1 = face_recognition.load_image_file(r'C:\Users\250498705\PycharmProjects\Project1\Resources\Xavier1.png')
img_Xavier1 = cv2.cvtColor(img_Xavier1, cv2.COLOR_RGB2BGR)
faceLocXavier1 = face_recognition.face_locations(img_Xavier1)[0]
encodeXavier1 = face_recognition.face_encodings(img_Xavier1)[0]
cv2.rectangle(img_Xavier1, (faceLocXavier1[3], faceLocXavier1[0]), (faceLocXavier1[1], faceLocXavier1[2]), (255, 0, 0), 2)


print("3")

# Create arrays of known face encodings and their names
known_face_encodings = [
    encode_CWY,
    encodeXavier1,

]
known_face_names = [
    "CWY",
    "Xavier1",
    "Xavier2"
]

print("4")

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

print("5")

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Only process every other frame of video to save time
    if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

            face_min_dis = min(face_distances)

            if face_min_dis < 0.5:

                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame
    # Display the results

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()