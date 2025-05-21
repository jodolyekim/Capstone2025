import 'dart:io';
import 'package:http/http.dart' as http;

Future<void> uploadImageToDjango(File imageFile) async {
  final uri = Uri.parse('http://10.0.2.2:8000/api/upload-image/');
  final request = http.MultipartRequest('POST', uri);

  request.files.add(await http.MultipartFile.fromPath('image', imageFile.path));
  final response = await request.send();

  if (response.statusCode == 200) {
    print("업로드 성공");
  } else {
    print("업로드 실패");
  }
}