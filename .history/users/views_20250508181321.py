@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_profile_partial(request):
    user = request.user
    profile = getattr(user, 'profile', None)

    if profile is None:
        profile = Profile.objects.create(
            user=user,
            name='',
            birth_date=date(2000, 1, 1),
            gender='미정',
            sexual_orientation='미정',
            communication_styles=[],
            latitude=0.0,
            longitude=0.0,
            match_distance_km=5,
        )

    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()

        # ✅ 프로필 설정 완료로 표시
        user.is_profile_set = True
        user.save()

        return Response({"message": "Profile updated successfully."}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
