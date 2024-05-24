import cv2

# Abre el video
video = cv2.VideoCapture(r'C:\Users\supra\PycharmProjects\pythonvideowall\publi.mp4')

# Obtiene las dimensiones del video
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Divide las dimensiones en 4 partes
part_width = width // 2
part_height = height // 2

# Define el codec y crea el objeto VideoWriter para cada parte
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out_part1 = cv2.VideoWriter('parte1.avi', fourcc, 20.0, (part_width, part_height))
out_part2 = cv2.VideoWriter('parte2.avi', fourcc, 20.0, (part_width, part_height))
out_part3 = cv2.VideoWriter('parte3.avi', fourcc, 20.0, (part_width, part_height))
out_part4 = cv2.VideoWriter('parte4.avi', fourcc, 20.0, (part_width, part_height))

while True:
    ret, frame = video.read()
    if not ret:
        break

    # Extrae cada parte del frame
    part1_frame = frame[0:part_height, 0:part_width]
    part2_frame = frame[0:part_height, part_width:width]
    part3_frame = frame[part_height:height, 0:part_width]
    part4_frame = frame[part_height:height, part_width:width]

    # Escribe cada parte en el archivo de video correspondiente
    out_part1.write(part1_frame)
    out_part2.write(part2_frame)
    out_part3.write(part3_frame)
    out_part4.write(part4_frame)

    cv2.imshow('Parte 1', part1_frame)
    cv2.imshow('Parte 2', part2_frame)
    cv2.imshow('Parte 3', part3_frame)
    cv2.imshow('Parte 4', part4_frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Libera los objetos VideoWriter y cierra el video
out_part1.release()
out_part2.release()
out_part3.release()
out_part4.release()
video.release()
cv2.destroyAllWindows()
