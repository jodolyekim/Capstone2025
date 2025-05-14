import 'dart:io';
import 'package:firebase_storage/firebase_storage.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;

Future<void> uploadProfileImage(String userId) async {
  final picker = ImagePicker();
  final picked = await picker.pickImage(source: ImageSource.gallery);
  if (picked == null) return;

  File file = File(picked.path);
  String fileName = 'profiles/$userId.jpg';

  try {
    final ref = FirebaseStorage.instance.ref().child(fileName);
    await ref.putFile(file);

    final downloadUrl = await ref.getDownloadURL();

    // Django로 업로드 URL 전송
    final res = await http.post(
      Uri.parse('http://<YOUR_BACKEND_HOST>/api/user/upload-profile/'),
      headers: {'Content-Type': 'application/json'},
      body: '{"user_id": "$userId", "profile_url": "$downloadUrl"}',
    );

    if (res.statusCode == 200) {
      print('URL 전송 성공');
    } else {
      print('서버 오류: ${res.body}');
    }
  } catch (e) {
    print('업로드 실패: $e');
  }
}
