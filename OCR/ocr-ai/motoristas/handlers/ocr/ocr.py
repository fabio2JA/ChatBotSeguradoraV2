# from typing import Any
# from paddleocr import PaddleOCR
# import cv2
# import numpy as np
# import os
# from django.conf import settings

# LETRAS_CORR = 'abcedfghijklmnopqrstuvwxyzáâàãéêèíîìóôòõúûùç123456789'
# REPLACE_CHARS = " /°.'ª;,"
# OCR = PaddleOCR(lang='pt', use_angle_cls=True, det_model_dir=os.path.join(settings.BASE_DIR, "det_db"))


# class TextCorrector:
#     def __init__(self, text: str):
#         self.text = text

#     def _insere_letra(self, new_word: list[str], new_texts: list[str], new_text: str, letra: str, n: int):
#         new_word.append(new_text[:n])
#         new_word.append(letra)
#         new_word.append(new_text[n:])
#         new_texts.append(''.join(new_word))
#         new_word.clear()

#     def _deleta_letra(self, new_word: list[str], new_texts: list[str], new_text: str, n: int):
#         new_word.append(new_text[:n])
#         new_word.append(new_text[n + 1:])
#         new_texts.append(''.join(new_word))
#         new_word.clear()

#     def _subistitui_letra(self, new_word: list[str], new_texts: list[str], new_text: str, letra: str, n: int):
#         new_word.append(new_text[:n])
#         new_word.append(letra)
#         new_word.append(new_text[n + 1:])
#         new_texts.append(''.join(new_word))
#         new_word.clear()

#     def correct_text(self, field_list: list[str]) -> str:
#         new_text = []
#         for letter in self.text:
#             if letter not in REPLACE_CHARS:
#                 new_text.append(letter.lower())

#         new_text = ''.join(new_text)
#         new_texts = [new_text]

#         new_word = []
#         for n in range(len(new_text) + 1):
#             self._deleta_letra(new_word, new_texts, new_text, n)

#             for letra in LETRAS_CORR:
#                 self._insere_letra(new_word, new_texts, new_text, letra, n)
#                 self._subistitui_letra(new_word, new_texts, new_text, letra, n)

#         for field in field_list:
#             if field in new_texts:
#                 return field


# class Finder:
#     def __init__(self, labels, fields: dict, fields_allow_multiple_vertical: list[str]):
#         self.texts_fields = {}
#         self.side_fields = {}
#         self.labels = labels
#         self.fields = fields
#         self.fields_allow_multiple_vertical = fields_allow_multiple_vertical

#     def find_below(self) -> tuple[dict, dict]:
#         for label in self.labels:
#             self.texts_fields[label['name']] = []
#             y_s = [cord[1] for cord in label['cords']]
#             label_y_min = min(y_s)
#             label_y_max = max(y_s)

#             x_s = [cord[0] for cord in label['cords']]
#             label_x_min = min(x_s)
#             label_x_max = max(x_s)

#             label_width = abs(label_x_max - label_x_min)

#             next_y = self._find_next(label_y_min, label_y_max)
#             self._find_fields(label, next_y, label_x_max, label_x_min, label_y_max, label_width)

#         return self.texts_fields, self.side_fields

#     def _find_next(self, label_y_min: int, label_y_max: int) -> int:
#         next_y = 10_000_000_000
#         for label_2 in self.labels:
#             y_s = [cord[1] for cord in label_2['cords']]
#             label_2_y_min = min(y_s)
#             label_2_y_max = max(y_s)

#             is_in_the_same_y = label_y_min < label_2_y_max and label_y_max > label_2_y_min

#             if (label_2_y_min > label_y_max
#                     and label_2_y_min != label_y_min
#                     and next_y == 10_000_000_000
#                     and not is_in_the_same_y):
#                 next_y = label_2_y_min
#         return next_y

#     def _find_fields(self, label: dict, next_y: int, label_x_max: int, 
#                      label_x_min: int, label_y_max: int, label_width: float):
#         for field in self.fields:
#             y_s = [cord[1] for cord in field['cords']]
#             field_y_min = min(y_s)
#             field_y_max = max(y_s)

#             x_s = [cord[0] for cord in field['cords']]
#             field_x_min = min(x_s)
#             field_x_max = max(x_s)

#             horizontal_allowed = field_x_min < label_x_max and field_x_max > label_x_min
#             if label_y_max < field_y_max and horizontal_allowed:
#                 x_medio = np.mean([p[0] for p in field['cords']])
#                 y_medio = np.mean([p[1] for p in field['cords']])
#                 center = (x_medio, y_medio)

#                 self.texts_fields[label['name']].append({'name': field['name'], 'center': center})
#                 self._find_side_fields(label, field_y_min, field_y_max, field_x_max, label_width)
#                 break

#     def _find_side_fields(self, label: dict, field_y_min: int, 
#                           field_y_max: int, field_x_max: int, label_width: float):
#         for field_2 in self.fields:
#             y_s =[cord[1] for cord in field_2['cords']]
#             field_2_y_min = min(y_s)

#             x_s = [cord[0] for cord in field_2['cords']]

#             field_2_y_max = max(y_s)
#             field_2_x_min = min(x_s)

#             fields_distance = abs(field_x_max - field_2_x_min)

#             distance_allowed = fields_distance < label_width

#             vertical_allowed = field_y_min < field_2_y_max and field_y_max > field_2_y_min
#             if (vertical_allowed and field_2_y_max != field_y_max 
#                 and field_2_x_min > field_x_max and distance_allowed):
#                 x_medio = np.mean([p[0] for p in field_2['cords']])
#                 y_medio = np.mean([p[1] for p in field_2['cords']])
#                 center = (x_medio, y_medio)
#                 self.side_fields.setdefault(label['name'], [])
#                 self.side_fields[label['name']].append({'name': field_2['name'], 'center': center})


# class OCRRecognitor:
#     def __init__(self, image, field_labels: list[str], fields_allow_multiple_vertical: list[str]):
#         self.image = image
#         self.field_labels = field_labels
#         self.result = self._preaper_ai()
#         self.fields = {}
#         self.fields_allow_multiple_vertical = fields_allow_multiple_vertical

#     def _preaper_ai(self) -> list:
#         # read
#         img = cv2.imread(self.image)
#         # pre processing
#         img_cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         # ai results
#         result = OCR.ocr(img, cls=True)
#         return result

#     def _get_texts(self) -> tuple[list[dict[str, str]], list[dict[str]]]:
#         labels = []
#         fields = []

#         for i in self.result[0]:
#             corrector = TextCorrector(i[1][0])
#             corrected_label = corrector.correct_text(self.field_labels)
#             if corrected_label is not None:
#                 labels.append(
#                     {'name': corrected_label, 'taxa_de_acertividade': i[1][1], 'cords': i[0]})
#             else:
#                 fields.append({'name': i[1][0], 'taxa_de_acertividade': i[1][1], 'cords': i[0]})
#         return labels, fields

#     def _organiza_texts(self, principal_labels: dict, side_labels: dict) -> dict:
#         new_fields = {}
#         principal_labels_centers = []
#         for labels in principal_labels.items():
#             new_fields[labels[0]] = []
#             for value in labels[1]:
#                 new_fields[labels[0]].append(value['name'])
#                 principal_labels_centers.append(value['center'])

#         for s_label_key, s_label_value in side_labels.items():
#             for side in s_label_value:
#               if side['center'] not in principal_labels_centers and s_label_key in new_fields:
#                 new_fields[s_label_key].append(side['name'])

#         return new_fields

#     def recognize(self, extracte_infos: dict) -> dict:
#         finder = Finder(*self._get_texts(), fields_allow_multiple_vertical=self.fields_allow_multiple_vertical)
#         principal_labels, side_labels = finder.find_below()

#         new_fields = self._organiza_texts(principal_labels, side_labels)
#         extracted = {}
#         extracted2 = {}
#         for key, value in extracte_infos.items():
#             if value in new_fields:
#                 extracted[key] = ' '.join(new_fields[value]).replace('  ', ' ')
#         for key, value in extracte_infos.items():
#             if key in extracted:
#                 extracted2[key] = extracted[key]
#             else:
#                 extracted2[key] = ''
#         return extracted2