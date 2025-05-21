import 'package:flutter/material.dart';
import 'manual_interest_page.dart';

class InterestPage extends StatefulWidget {
  final VoidCallback onFinish;
  const InterestPage({required this.onFinish, Key? key}) : super(key: key);

  @override
  State<InterestPage> createState() => _InterestPageState();
}

class _InterestPageState extends State<InterestPage> {
  final TextEditingController _introController = TextEditingController();
  List<String> extractedKeywords = [];
  bool isLoading = false;
  String error = '';

  void extractKeywords() async {
    setState(() => isLoading = true);
    // GPT 호출 및 키워드 추출 로직
    await Future.delayed(const Duration(seconds: 1));
    setState(() {
      extractedKeywords = ['운동', '음악', '책'];
      isLoading = false;
    });
  }

  void goToManualSelection() {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => InterestManualPage(
          onFinish: widget.onFinish, // 마지막 완료는 상위 위젯에서 정의
        ),
      ),
    );
  }

  Widget _buildKeywordButtons() {
    return Wrap(
      spacing: 8,
      children: extractedKeywords
          .map((k) => Chip(label: Text(k)))
          .toList(),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('자기소개 & 키워드 추출')),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('자기소개 (최소 20자)', style: TextStyle(fontSize: 16)),
              const SizedBox(height: 8),
              TextField(
                controller: _introController,
                maxLines: 6,
                minLines: 3,
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  hintText: '자신의 관심사, 취향, 성격 등을 자유롭게 적어주세요.',
                ),
              ),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: isLoading ? null : extractKeywords,
                child: isLoading
                    ? const CircularProgressIndicator()
                    : const Text('GPT로 키워드 추출'),
              ),
              if (error.isNotEmpty)
                Padding(
                  padding: const EdgeInsets.only(top: 12),
                  child: Text(error, style: const TextStyle(color: Colors.red)),
                ),
              const SizedBox(height: 24),
              _buildKeywordButtons(),
              if (extractedKeywords.isNotEmpty)
                Center(
                  child: ElevatedButton(
                    onPressed: goToManualSelection,
                    child: const Text('추천 키워드 선택으로 이동'),
                  ),
                )
            ],
          ),
        ),
      ),
    );
  }
}
