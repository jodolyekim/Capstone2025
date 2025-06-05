import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class GuardianUploadStep extends StatefulWidget {
  final VoidCallback onFinish;
  final VoidCallback onBack;
  const GuardianUploadStep({super.key, required this.onFinish, required this.onBack});

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

  Widget _previewImage(File? file, String label, bool isFamily) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          "${label} 업로드",
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 10),
        GestureDetector(
          onTap: () => _pickFile(isFamily),
          child: file != null
          ? Image.file(file, width: 300, height: 150, fit: BoxFit.cover)
          : Container(
              width: 300,
              height: 150,
              color: Colors.grey[300],
              child: const Icon(Icons.add_a_photo, size: 32),
            ),
        ),
        TextButton(
          onPressed: file != null
              ? () {
            showDialog(
              context: context,
              builder: (_) => Dialog(
                child: InteractiveViewer( // 확대/이동 가능
                  child: Image.file(file),
                ),
              ),
            );
          }
              : null, // 파일이 없으면 비활성화
          child: Text("${label} 미리보기 클릭"),
        ),
        const SizedBox(height: 10),
      ],
    );

  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _previewImage(familyCert, '가족관계증명서', true),
        _previewImage(disabilityCert, '장애인등록증', false),

        const Text("파일을 교체하실 때는 사진을 다시 클릭하세요!"),
        const Spacer(),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            ElevatedButton(
                onPressed: widget.onBack,
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
                  textStyle: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
                child: const Text('이전')
            ),
            ElevatedButton(
              onPressed: _uploadFiles,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
                textStyle: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              ),
              child: const Text('파일 업로드 완료'),
            ),
          ],
        ),


      ],
    );
  }
}