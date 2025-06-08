import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class InterestManualPage extends StatefulWidget {
  final VoidCallback onFinish;
  final List<String> preselectedKeywords;

  const InterestManualPage({
    required this.onFinish,
    required this.preselectedKeywords,
    Key? key,
  }) : super(key: key);

  @override
  State<InterestManualPage> createState() => _InterestManualPageState();
}

class _InterestManualPageState extends State<InterestManualPage> {
  Map<String, List<String>> recommendedKeywords = {};
  String selectedCategory = '';
  Set<String> selectedKeywords = {};
  bool isLoading = true;
  String searchQuery = '';

  @override
  void initState() {
    super.initState();
    selectedKeywords = widget.preselectedKeywords.toSet();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      fetchRecommendedKeywords();
    });
  }

  Future<void> fetchRecommendedKeywords() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('accessToken');
      final email = prefs.getString('userEmail');

      if (token == null || email == null) {
        throw Exception('accessToken 또는 userEmail 없음');
      }

      final url = Uri.parse('http://10.0.2.2:8000/api/interest/keywords/manual/');
      final res = await http.get(
        url,
        headers: {'Authorization': 'Bearer $token'},
      ).timeout(const Duration(seconds: 7));

      if (res.statusCode == 200) {
        final data = json.decode(utf8.decode(res.bodyBytes));
        if (data is Map<String, dynamic>) {
          final parsed = <String, List<String>>{};
          data.forEach((key, value) {
            if (value is List) {
              parsed[key] = List<String>.from(value.map((e) => e.toString()));
            }
          });

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
      print('❌ 키워드 로딩 실패: $e');
      if (mounted) {
        setState(() => isLoading = false);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('추천 키워드를 불러오지 못했습니다.\n$e')),
        );
      }
    }
  }

  Future<void> saveSelectedKeywords() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('accessToken');
      final email = prefs.getString('userEmail');

      if (token == null || email == null) {
        throw Exception('accessToken 또는 userEmail 없음');
      }

      final url = Uri.parse('http://10.0.2.2:8000/api/interest/keywords/manual/');
      final res = await http.post(
        url,
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
        body: json.encode({
          'category': selectedCategory,
          'keywords': selectedKeywords.toList(),
        }),
      );

      if (res.statusCode != 201) {
        throw Exception('키워드 저장 실패: ${res.statusCode}');
      }

      final completeUrl = Uri.parse('http://10.0.2.2:8000/api/profile/set-complete/');
      final completeRes = await http.patch(
        completeUrl,
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
      );

      if (completeRes.statusCode != 200) {
        throw Exception('프로필 완료 처리 실패: ${completeRes.statusCode}');
      }

      if (!mounted) return;
      Navigator.pushNamedAndRemoveUntil(context, '/', (route) => false);
      await Future.delayed(const Duration(milliseconds: 300));

      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text(
              '회원가입 승인을 기다려주세요.\n회원가입이 승인된 후에 로그인을 하시면 채팅 기능을 사용할 수 있습니다.',
              textAlign: TextAlign.center,
            ),
            duration: Duration(seconds: 5),
          ),
        );
      }
    } catch (e) {
      print('❌ 저장 실패: $e');
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('저장 또는 완료 중 오류 발생: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }

    final categoryTabs = recommendedKeywords.keys.toList();
    final allKeywords = recommendedKeywords[selectedCategory] ?? [];
    final filteredKeywords = searchQuery.isEmpty
        ? allKeywords
        : allKeywords.where((k) => k.contains(searchQuery)).toList();

    return Scaffold(
      appBar: AppBar(title: const Text('관심 키워드 선택')),
      body: Container(
        color: const Color(0xFFF9F6FC),
        child: Column(
          children: [
            SizedBox(
              height: 60,
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: 12),
                itemCount: categoryTabs.length,
                itemBuilder: (context, index) {
                  final category = categoryTabs[index];
                  final isSelected = category == selectedCategory;
                  return Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 6),
                    child: ChoiceChip(
                      label: Text(category, style: const TextStyle(fontSize: 16)),
                      selected: isSelected,
                      onSelected: (_) {
                        setState(() {
                          selectedCategory = category;
                          searchQuery = '';
                        });
                      },
                      selectedColor: Colors.deepPurple[100],
                      backgroundColor: Colors.grey[200],
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
                    ),
                  );
                },
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(12),
              child: TextField(
                onChanged: (value) => setState(() => searchQuery = value),
                decoration: InputDecoration(
                  hintText: '키워드를 검색하세요',
                  prefixIcon: const Icon(Icons.search),
                  filled: true,
                  fillColor: Colors.white,
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                  focusedBorder: OutlineInputBorder(
                    borderSide: const BorderSide(color: Colors.deepPurple),
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
              ),
            ),
            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.symmetric(horizontal: 12),
                child: Wrap(
                  spacing: 8,
                  runSpacing: 8,
                  children: filteredKeywords.map((keyword) {
                    final isSelected = selectedKeywords.contains(keyword);
                    return FilterChip(
                      label: Text(keyword, style: const TextStyle(fontSize: 15)),
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
                      selectedColor: Colors.deepPurple[200],
                      checkmarkColor: Colors.white,
                      backgroundColor: Colors.grey[200],
                      labelStyle: TextStyle(
                        fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                      ),
                    );
                  }).toList(),
                ),
              ),
            ),
            const Divider(height: 20, thickness: 1),
            Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  if (selectedKeywords.isNotEmpty) ...[
                    Align(
                      alignment: Alignment.centerLeft,
                      child: Text('📝 선택한 키워드: ${selectedKeywords.length} / 10', style: TextStyle(fontWeight: FontWeight.bold)),
                    ),
                    const SizedBox(height: 8),
                    Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: selectedKeywords
                          .map((k) => Chip(label: Text(k), deleteIcon: const Icon(Icons.close), onDeleted: () {
                        setState(() => selectedKeywords.remove(k));
                      }))
                          .toList(),
                    ),
                  ],
                  const SizedBox(height: 8),
                  ElevatedButton(
                    onPressed: selectedKeywords.length >= 3 ? saveSelectedKeywords : null,
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
                      textStyle: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    child: const Text('선택 키워드 저장'),
                  ),
                ],
              ),
            )
          ],
        ),
      ),
    );
  }
}