import 'dart:io';
import 'package:firebase_storage/firebase_storage.dart';
import 'package:firebase_auth/firebase_auth.dart';

Future<String?> uploadProfileImage(File imageFile) async {
  final user = FirebaseAuth.instance.currentUser;
  final ref = FirebaseStorage.instance.ref().child('profiles/\${user!.uid}.jpg');

  final uploadTask = await ref.putFile(imageFile);
  return await uploadTask.ref.getDownloadURL();
}