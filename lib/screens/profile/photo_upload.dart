import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:firebase_storage/firebase_storage.dart';
import 'package:path/path.dart' as path;

class PhotoUploadScreen extends StatefulWidget {
  final bool returnUrlOnPop;

  const PhotoUploadScreen({super.key, this.returnUrlOnPop = false});

  @override
  State<PhotoUploadScreen> createState() => _PhotoUploadScreenState();
}

class _PhotoUploadScreenState extends State<PhotoUploadScreen> {
  File? _selectedImage;
  bool _isUploading = false;
  String? _uploadedImageUrl;

  Future<void> _pickImage() async {
    final ImagePicker picker = ImagePicker();
    final XFile? image = await picker.pickImage(source: ImageSource.gallery);

    if (image != null) {
      setState(() {
        _selectedImage = File(image.path);
      });
    }
  }

  Future<void> _uploadToFirebase() async {
    if (_selectedImage == null) return;

    setState(() => _isUploading = true);

    try {
      final fileName = path.basename(_selectedImage!.path);
      final storageRef = FirebaseStorage.instance.ref().child('profiles/$fileName');

      final uploadTask = await storageRef.putFile(_selectedImage!);
      final url = await uploadTask.ref.getDownloadURL();

      setState(() {
        _uploadedImageUrl = url;
        _isUploading = false;
      });

      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('업로드 성공')),
        );
      }

      if (widget.returnUrlOnPop && context.mounted) {
        Navigator.pop(context, url); // ✅ 업로드 성공 시 URL 반환
      }

    } catch (e) {
      setState(() => _isUploading = false);
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('업로드 실패: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('사진 업로드')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            _selectedImage != null
                ? Image.file(_selectedImage!, height: 200)
                : const Placeholder(fallbackHeight: 200),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _pickImage,
              child: const Text('사진 선택'),
            ),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: _isUploading ? null : _uploadToFirebase,
              child: _isUploading
                  ? const CircularProgressIndicator()
                  : const Text('업로드'),
            ),
            if (_uploadedImageUrl != null && !widget.returnUrlOnPop) ...[
              const SizedBox(height: 20),
              Text('URL: $_uploadedImageUrl'),
            ]
          ],
        ),
      ),
    );
  }
}
