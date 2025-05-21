import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class GuardianUploadStep extends StatefulWidget {
  final VoidCallback onFinish;

  const GuardianUploadStep({super.key, required this.onFinish});

  @override
  State<GuardianUploadStep> createState() => _GuardianUploadStepState();
}

class _GuardianUploadStepState extends State<GuardianUploadStep> {
  File? familyCert;
  File? disabilityCert;

  final picker = ImagePicker();

  Future<void> _pickFile(bool isFamily) async {
    final picked = await picker.pickImage(source: ImageSource.gallery);
    if (picked != null) {
      setState(() {
        if (isFamily) {
          familyCert = File(picked.path);
        } else {
          disabilityCert = File(picked.path);
        }
      });
    }
  }

  Future<void> _uploadFiles() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('accessToken');
    if (token == null) return;

    final url = Uri.parse('http://10.0.2.2:8000/api/guardian/upload/');
    var request = http.MultipartRequest('POST', url);
    request.headers['Authorization'] = 'Bearer $token';

    if (familyCert != null) {
      request.files.add(await http.MultipartFile.fromPath('family_certificate', familyCert!.path));
    }
    if (disabilityCert != null) {
      request.files.add(await http.MultipartFile.fromPath('disability_certificate', disabilityCert!.path));
    }

    final res = await request.send();
    if (res.statusCode == 200) {
      if (context.mounted) ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('파일 업로드가 완료되었습니다.')),
      );
      widget.onFinish();
    } else {
      if (context.mounted) ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('파일 업로드에 실패했습니다.')),
      );
    }
  }

  Widget _previewImage(File? file, String label) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label),
        const SizedBox(height: 8),
        file != null
            ? Image.file(file, width: 150, height: 150, fit: BoxFit.cover)
            : const Text('선택된 파일 없음'),
        const SizedBox(height: 16),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('증명서 업로드')),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            ElevatedButton(
              onPressed: () => _pickFile(true),
              child: Text(familyCert == null ? '가족관계증명서 선택' : '가족관계증명서 다시 선택'),
            ),
            _previewImage(familyCert, '가족관계증명서 미리보기'),
            ElevatedButton(
              onPressed: () => _pickFile(false),
              child: Text(disabilityCert == null ? '장애인등록증 선택' : '장애인등록증 다시 선택'),
            ),
            _previewImage(disabilityCert, '장애인등록증 미리보기'),
            const Spacer(),
            ElevatedButton(
              onPressed: _uploadFiles,
              child: const Text('파일 업로드 완료'),
            )
          ],
        ),
      ),
    );
  }
}