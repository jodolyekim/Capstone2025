// step4 - 보호자 기본 정보 입력 → 증명서 업로드로 이동

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'guardian_upload.dart';

class GuardianInfoStep extends StatefulWidget {
  final VoidCallback onNext;
  final VoidCallback onBack;

  const GuardianInfoStep({super.key, required this.onNext, required this.onBack});

  @override
  State<GuardianInfoStep> createState() => _GuardianInfoStepState();
}

class _GuardianInfoStepState extends State<GuardianInfoStep> {
  final _nameController = TextEditingController();
  final _phoneController = TextEditingController();
  DateTime? _birthDate;
  String? _relation;

  Future<void> _submitGuardianInfo() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('accessToken');
    if (token == null) return;

    // 1단계: 프로필 정보에 보호자 항목 저장
    final profileUrl = Uri.parse('http://10.0.2.2:8000/api/profile/update/');
    final profileBody = {
      '_protector_info_name': _nameController.text,
      '_protector_info_phone': _phoneController.text,
      '_protector_info_birth_date': _birthDate?.toIso8601String().split('T')[0],
      '_protector_info_relationship': _relation,
    };

    final profileRes = await http.patch(
      profileUrl,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode(profileBody),
    );

    if (profileRes.statusCode != 200) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('보호자 정보를 저장하는 데 실패했습니다.')),
      );
      return;
    }

    // 2단계: Guardian 객체 생성 (이미 있으면 넘어감)
    final guardianUrl = Uri.parse('http://10.0.2.2:8000/api/guardian/create/');
    final guardianBody = {
      'name': _nameController.text,
      'phone': _phoneController.text,
      'relation': _relation,
    };

    final guardianRes = await http.post(
      guardianUrl,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode(guardianBody),
    );

    if (guardianRes.statusCode != 201 && guardianRes.statusCode != 400) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('보호자 모델 생성 실패')),
      );
      return;
    }

    // 3단계: 증명서 업로드 화면 이동
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => GuardianUploadStep(
          onFinish: () {
            Navigator.pushReplacementNamed(context, '/');
          },
        ),
      ),
    );
  }

  void _selectBirthDate() async {
    final picked = await showDatePicker(
      context: context,
      initialDate: DateTime(1980),
      firstDate: DateTime(1900),
      lastDate: DateTime.now(),
    );
    if (picked != null) {
      setState(() {
        _birthDate = picked;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('보호자 정보 입력')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(controller: _nameController, decoration: const InputDecoration(labelText: '보호자 이름')),
            TextField(controller: _phoneController, decoration: const InputDecoration(labelText: '보호자 전화번호')),
            const SizedBox(height: 12),
            Row(
              children: [
                const Text('보호자 생년월일: '),
                Text(_birthDate == null ? '미지정' : _birthDate!.toLocal().toString().split(' ')[0]),
                TextButton(onPressed: _selectBirthDate, child: const Text('날짜 선택')),
              ],
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              value: _relation,
              items: ['아빠', '엄마', '형제자매'].map((relation) {
                return DropdownMenuItem(value: relation, child: Text(relation));
              }).toList(),
              onChanged: (val) => setState(() => _relation = val),
              decoration: const InputDecoration(labelText: '관계'),
            ),
            const Spacer(),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                ElevatedButton(onPressed: widget.onBack, child: const Text('이전')),
                ElevatedButton(onPressed: _submitGuardianInfo, child: const Text('다음')),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
