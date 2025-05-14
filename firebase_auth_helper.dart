import 'package:firebase_auth/firebase_auth.dart';

Future<String?> getFirebaseIdToken() async {
  User? user = FirebaseAuth.instance.currentUser;
  if (user == null) {
    await FirebaseAuth.instance.signInWithEmailAndPassword(
      email: 'test@example.com',
      password: '123456',
    );
    user = FirebaseAuth.instance.currentUser;
  }
  return await user?.getIdToken();
}