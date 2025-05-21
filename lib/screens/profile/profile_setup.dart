import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
// import 'AuthCompletePage.dart';
import 'guardian.dart';
import 'guardian_upload.dart';
import 'package:front_integration/screens/interest/interest_page.dart';
import 'package:front_integration/screens/interest/manual_interest_page.dart';


class ProfileSetupScreen extends StatefulWidget {
  final int initialStep;
  final Map<String, dynamic>? existingData;

  const ProfileSetupScreen({
    super.key,
    this.initialStep = 0,
    this.existingData,
  });

  @override
  State<ProfileSetupScreen> createState() => _ProfileSetupScreenState();
}

class _ProfileSetupScreenState extends State<ProfileSetupScreen> {
  late int _currentStep;

  final _nameController = TextEditingController();
  DateTime? _birthdate;
  String? _gender;
  String? _orientation;
  List<String> _communicationStyles = [];
  Position? _location;
  double _distance = 5;

  @override
  void initState() {
    super.initState();
    _currentStep = widget.initialStep;
    final data = widget.existingData;
    if (data != null) {
      _nameController.text = data['_name'] ?? '';
      if (data['_birthYMD'] != null) {
        _birthdate = DateTime.tryParse(data['_birthYMD']);
      }
      _gender = data['_gender'];
      _orientation = data['_sex_orientation'];
      _communicationStyles = List<String>.from(data['_communication_way'] ?? []);
      if (data['_current_location'] != null &&
          data['_current_location']['lat'] != null &&
          data['_current_location']['lon'] != null) {
        _location = Position(
          latitude: data['_current_location']['lat'],
          longitude: data['_current_location']['lon'],
          timestamp: DateTime.now(),
          accuracy: 0,
          altitude: 0,
          heading: 0,
          speed: 0,
          speedAccuracy: 0,
          altitudeAccuracy: 0,
          headingAccuracy: 0,
          floor: 0,
          isMocked: false,
        );
      }
      _distance = (data['_match_distance'] ?? 5).toDouble();
    }
  }

  Future<void> _saveStepData() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('accessToken');
    if (token == null) return;

    final url = Uri.parse('http://10.0.2.2:8000/api/profile/update/');
    Map<String, dynamic> body = {};

    if (_currentStep == 0) {
      body = {
        '_name': _nameController.text,
        '_birthYMD': _birthdate?.toIso8601String().split('T')[0],
        '_gender': _gender,
        '_sex_orientation': _orientation,
      };
    } else if (_currentStep == 1) {
      body = {
        '_communication_way': _communicationStyles,
      };
    } else if (_currentStep == 2) {
      body = {
        '_current_location_lat': _location?.latitude,
        '_current_location_lon': _location?.longitude,
        '_match_distance': _distance.round(),
      };
    }

    await http.patch(
      url,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode(body),
    );
  }

  void _goNext() async {
    await _saveStepData();
    if (_currentStep < 4) {
      setState(() => _currentStep++);
    } else {
      if (context.mounted) Navigator.pushReplacementNamed(context, '/');
    }
  }

  void _goBack() {
    if (_currentStep > 0) {
      setState(() => _currentStep--);
    }
  }

  bool _isStepValid() {
    switch (_currentStep) {
      case 0:
        return _nameController.text.isNotEmpty &&
            _birthdate != null &&
            _gender != null &&
            _orientation != null;
      case 1:
        return _communicationStyles.isNotEmpty;
      case 2:
        return _location != null && _distance >= 5;
      default:
        return true;
    }
  }

  void _goToInterestFlow() {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => InterestPage(
          onFinish: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => InterestManualPage(
                  onFinish: () {
                    if (context.mounted) Navigator.pushReplacementNamed(context, '/');
                  },
                ),
              ),
            );
          },
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    List<Widget> steps = [
      Step1BasicInfo(
        nameController: _nameController,
        birthdate: _birthdate,
        gender: _gender,
        orientation: _orientation,
        onChanged: (birth, gen, ori) {
          setState(() {
            _birthdate = birth;
            _gender = gen;
            _orientation = ori;
          });
        },
      ),
      Step2Communication(
        selectedOptions: _communicationStyles,
        onChanged: (list) => setState(() => _communicationStyles = list),
      ),
      Step3LocationDistance(
        location: _location,
        onLocationRetrieved: (pos) => setState(() => _location = pos),
        distance: _distance,
        onDistanceChanged: (val) => setState(() => _distance = val),
      ),
      GuardianInfoStep(
        onNext: () => setState(() => _currentStep++),
        onBack: _goBack,
      ),
      GuardianUploadStep(
        onFinish: _goToInterestFlow,
      ),
    ];

    return Scaffold(
      appBar: AppBar(
        title: Text('프로필 설정 (${_currentStep + 1}/${steps.length})'),
        automaticallyImplyLeading: false,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            Expanded(child: steps[_currentStep]),
            if (_currentStep < 3)
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  if (_currentStep > 0)
                    ElevatedButton(onPressed: _goBack, child: const Text('이전')),
                  ElevatedButton(
                    onPressed: _isStepValid() ? _goNext : null,
                    child: Text('다음'),
                  ),
                ],
              ),
          ],
        ),
      ),
    );
  }
}



// [1단계] 이름, 생년월일, 성별, 성적 지향 입력
class Step1BasicInfo extends StatelessWidget {
  final TextEditingController nameController;
  final DateTime? birthdate;
  final String? gender;
  final String? orientation;
  final Function(DateTime?, String?, String?) onChanged;

  const Step1BasicInfo({
    super.key,
    required this.nameController,
    required this.birthdate,
    required this.gender,
    required this.orientation,
    required this.onChanged,
  });

  // 생일 선택 다이얼로그
  Future<void> _pickBirthdate(BuildContext context) async {
    final picked = await showDatePicker(
      context: context,
      initialDate: DateTime(DateTime.now().year - 20),
      firstDate: DateTime(1900),
      lastDate: DateTime.now(),
    );
    if (picked != null) onChanged(picked, gender, orientation);
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        TextField(controller: nameController, decoration: const InputDecoration(labelText: '이름')),
        ElevatedButton(
          onPressed: () => _pickBirthdate(context),
          child: const Text('생년월일 선택'),
        ),
        if (birthdate != null)
          Text('선택한 날짜: ${birthdate!.toLocal().toIso8601String().split("T")[0]}'),
        const Text('성별 선택'),
        ...['남성', '여성'].map((val) => RadioListTile(
          value: val,
          groupValue: gender,
          title: Text(val),
          onChanged: (v) => onChanged(birthdate, v, orientation),
        )),
        const Text('성적 지향'),
        ...[
          '이성을 만나고 싶어요',
          '동성을 만나고 싶어요',
          '모두 만나고 싶어요'
        ].map((val) => RadioListTile(
          value: val,
          groupValue: orientation,
          title: Text(val),
          onChanged: (v) => onChanged(birthdate, gender, v),
        )),
      ],
    );
  }
}

// [2단계] 커뮤니케이션 스타일 선택 (복수 선택 가능)
class Step2Communication extends StatelessWidget {
  final List<String> selectedOptions;
  final ValueChanged<List<String>> onChanged;

  const Step2Communication({
    super.key,
    required this.selectedOptions,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    final options = [
      '짧은 문장으로 대화하고 싶어요',
      '답장이 빠르면 좋겠어요',
      '답장이 느려도 괜찮아요',
      '관심사만 이야기 하고 싶어요',
      '천천히 알아가고 싶어요',
      '대화가 끊기기 전에 미리 말해줬으면 좋겠어요',
      '문자로 대화하는 걸 좋아해요',
      '부드럽게 대화하고 싶어요',
      '서로의 말에 공감의 메시지를 주고받고 싶어요'
    ];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('채팅 시 선호하는 대화 방식 (복수 선택 가능)'),
        ...options.map((option) => CheckboxListTile(
          title: Text(option),
          value: selectedOptions.contains(option),
          onChanged: (val) {
            final updated = List<String>.from(selectedOptions);
            val! ? updated.add(option) : updated.remove(option);
            onChanged(updated);
          },
        )),
      ],
    );
  }
}

// [3단계] 위치 권한 요청 및 거리 설정
class Step3LocationDistance extends StatelessWidget {
  final Position? location;
  final ValueChanged<Position> onLocationRetrieved;
  final double distance;
  final ValueChanged<double> onDistanceChanged;

  const Step3LocationDistance({
    super.key,
    required this.location,
    required this.onLocationRetrieved,
    required this.distance,
    required this.onDistanceChanged,
  });

  // 위치 권한 요청 및 현재 위치 가져오기
  Future<void> _getLocation(BuildContext context) async {
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      await Geolocator.openLocationSettings();
      return;
    }
    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.deniedForever || permission == LocationPermission.denied) {
        return;
      }
    }
    final position = await Geolocator.getCurrentPosition();
    onLocationRetrieved(position);
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('위치 권한 및 매칭 거리 설정'),
        ElevatedButton(onPressed: () => _getLocation(context), child: const Text('내 위치 불러오기')),
        if (location != null)
          const Padding(
            padding: EdgeInsets.only(top: 12),
            child: Text('✅ 위치 설정이 완료되었습니다.', style: TextStyle(color: Colors.green)),
          ),
        const Text('매칭 희망 거리 (5km ~ 600km)'),
        Slider(
          value: distance,
          min: 5,
          max: 600,
          divisions: 119,
          label: '${distance.round()} km',
          onChanged: onDistanceChanged,
        ),
        Text('현재 선택: ${distance.round()} km'),
      ],
    );
  }
}