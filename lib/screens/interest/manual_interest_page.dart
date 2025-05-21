import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class InterestManualPage extends StatefulWidget {
  final VoidCallback onFinish;
  const InterestManualPage({required this.onFinish, Key? key}) : super(key: key);

  @override
  State<InterestManualPage> createState() => _InterestManualPageState();
}

class _InterestManualPageState extends State<InterestManualPage> {
  Map<String, List<String>> recommendedKeywords = {};
  String selectedCategory = '';
  Set<String> selectedKeywords = {};
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      fetchRecommendedKeywords();
    });
  }

  Future<void> fetchRecommendedKeywords() async {
    try {
      print('⏳ 키워드 로딩 시작');
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('accessToken');
      if (token == null) throw Exception('accessToken 없음');

      final url = Uri.parse('http://10.0.2.2:8000/api/interest/manual-keywords/');
      final res = await http.get(url, headers: {
        'Authorization': 'Bearer $token'
      }).timeout(const Duration(seconds: 7));

      print('📥 응답 상태: ${res.statusCode}');
      print('📥 응답 본문: ${res.body}');

      if (res.statusCode == 200) {
        final data = json.decode(utf8.decode(res.bodyBytes));
        print('✅ JSON 파싱 성공: $data');
        print('✅ 데이터 타입: ${data.runtimeType}');

        if (data is Map<String, dynamic>) {
          Map<String, List<String>> parsed = {};
          data.forEach((key, value) {
            if (value is List) {
              parsed[key] = List<String>.from(value.map((e) => e.toString()));
            } else {
              print('⚠️ 무시된 항목: $key → $value');
            }
          });

          print('🔥 최종 recommendedKeywords: $parsed');
          if (parsed.isEmpty) {
            print('🚨 경고: 추천 키워드가 비어있습니다');
          }

          setState(() {
            recommendedKeywords = parsed;
            selectedCategory = parsed.keys.isNotEmpty ? parsed.keys.first : '';
            isLoading = false;
          });
        } else {
          throw Exception('받은 데이터가 Map 형태가 아님');
        }
      } else {
        throw Exception('추천 키워드 응답 실패: ${res.statusCode}');
      }
    } catch (e) {
      print('❌ 추천 키워드 로딩 실패: $e');
      if (mounted) {
        setState(() => isLoading = false);
      }
      if (context.mounted) ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('추천 키워드를 불러오지 못했습니다.\n$e')),
      );
    }
  }

  Future<void> saveSelectedKeywords() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('accessToken');
      if (token == null) throw Exception('accessToken 없음');

      final url = Uri.parse('http://10.0.2.2:8000/api/interest/save-manual-keywords/');
      final res = await http.post(
          url,
          headers: {
            'Authorization': 'Bearer $token',
            'Content-Type': 'application/json'
          },
          body: json.encode({
            'category': selectedCategory,
            'keywords': selectedKeywords.toList()
          })
      );

      if (res.statusCode == 201) {
        if (context.mounted) ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('키워드가 저장되었습니다.')),
        );
        widget.onFinish();
      } else {
        throw Exception('저장 실패: ${res.statusCode}');
      }
    } catch (e) {
      print('❌ 키워드 저장 실패: $e');
      if (context.mounted) ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('저장 중 오류 발생: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }

    final categoryTabs = recommendedKeywords.keys.toList();
    final keywords = recommendedKeywords[selectedCategory] ?? [];

    return Scaffold(
      appBar: AppBar(title: const Text('관심 키워드 선택')),
      body: Column(
        children: [
          SizedBox(
            height: 50,
            child: ListView.builder(
              scrollDirection: Axis.horizontal,
              itemCount: categoryTabs.length,
              itemBuilder: (context, index) {
                final category = categoryTabs[index];
                final isSelected = category == selectedCategory;
                return Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 8),
                  child: ChoiceChip(
                    label: Text(category),
                    selected: isSelected,
                    onSelected: (_) {
                      setState(() => selectedCategory = category);
                    },
                  ),
                );
              },
            ),
          ),
          const SizedBox(height: 20),
          Wrap(
            spacing: 10,
            children: keywords.map((keyword) {
              final isSelected = selectedKeywords.contains(keyword);
              return FilterChip(
                label: Text(keyword),
                selected: isSelected,
                onSelected: (bool selected) {
                  setState(() {
                    if (selected && selectedKeywords.length < 10) {
                      selectedKeywords.add(keyword);
                    } else {
                      selectedKeywords.remove(keyword);
                    }
                  });
                },
              );
            }).toList(),
          ),
          const Spacer(),
          Text('선택한 키워드: ${selectedKeywords.length} / 10'),
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 16.0),
            child: ElevatedButton(
              onPressed: selectedKeywords.length >= 3 ? saveSelectedKeywords : null,
              child: const Text('선택 키워드 저장'),
            ),
          )
        ],
      ),
    );
  }
}