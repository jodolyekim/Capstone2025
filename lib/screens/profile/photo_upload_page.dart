import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class PhotoUploadStep extends StatefulWidget {
  final VoidCallback onComplete;

  const PhotoUploadStep({super.key, required this.onComplete});

  @override
  State<PhotoUploadStep> createState() => _PhotoUploadStepState();
}

class _PhotoUploadStepState extends State<PhotoUploadStep> {
  final List<File> _images = [];
  bool _uploading = false;

  Future<void> _pickImage() async {
    if (_images.length >= 6) return;

    final picker = ImagePicker();
    final picked = await picker.pickImage(source: ImageSource.gallery);
    if (picked != null) {
      setState(() => _images.add(File(picked.path)));
    }
  }

  Future<void> _uploadImages() async {
    if (_images.length < 2) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('사진은 최소 2장 이상 필요합니다.')),
      );
      return;
    }

    setState(() => _uploading = true);
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('accessToken');

    if (token == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('로그인이 필요합니다.')),
      );
      setState(() => _uploading = false);
      return;
    }

    for (final image in _images) {
      final uri = Uri.parse('http://10.0.2.2:8000/api/photos/upload-image/');
      final request = http.MultipartRequest('POST', uri);
      request.files.add(await http.MultipartFile.fromPath('image', image.path));
      request.headers['Authorization'] = 'Bearer $token';

      final response = await request.send();
      if (response.statusCode != 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('사진 업로드 중 오류 발생')),
        );
        setState(() => _uploading = false);
        return;
      }
    }

    setState(() => _uploading = false);
    widget.onComplete();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('본인 사진을 최소 2장, 최대 6장 업로드해주세요.'),
        const SizedBox(height: 12),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          children: [
            ..._images.map((img) =>
              Image.file(img, width: 100, height: 100, fit: BoxFit.cover)),
            if (_images.length < 6)
              GestureDetector(
                onTap: _pickImage,
                child: Container(
                  width: 100,
                  height: 100,
                  color: Colors.grey[300],
                  child: const Icon(Icons.add_a_photo, size: 32),
                ),
              ),
          ],
        ),
        const SizedBox(height: 20),
        ElevatedButton(
          onPressed: (_images.length >= 2 && !_uploading) ? _uploadImages : null,
          child: _uploading
              ? const CircularProgressIndicator()
              : const Text('사진 업로드 완료'),
        ),
      ],
    );
  }
}
