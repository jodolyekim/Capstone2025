import 'package:flutter/material.dart';

class UserCard extends StatelessWidget {
  final Map<String, dynamic> user;
  final String currentUserEmail;
  final void Function() onAccept;
  final void Function() onReject;

  const UserCard({
    super.key,
    required this.user,
    required this.currentUserEmail,
    required this.onAccept,
    required this.onReject,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      elevation: 8,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Image.network(user['photoUrl'] ?? '', height: 150),
            const SizedBox(height: 12),
            Text(user['name'] ?? '알 수 없음',
                style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
            const SizedBox(height: 6),
            Text("관심 키워드: ${(user['keywords'] as List<dynamic>).join(', ')}"),
            Text("대화 스타일: ${user['chatStyle'] ?? ''}"),
            Text("거리: ${user['distance'] ?? ''}"),
            const SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton.icon(
                  icon: const Icon(Icons.check),
                  label: const Text('💚 수락'),
                  onPressed: onAccept,
                ),
                ElevatedButton.icon(
                  icon: const Icon(Icons.close),
                  label: const Text('❌ 거절'),
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.redAccent),
                  onPressed: onReject,
                ),
              ],
            ),
            const SizedBox(height: 12),
            const Text(
              "⚠️ 먼저 거절하면 상대는 더 이상 응답할 수 없어요.",
              style: TextStyle(color: Colors.red, fontSize: 12),
            ),
          ],
        ),
      ),
    );
  }
}
