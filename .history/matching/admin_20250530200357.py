from django.contrib import admin
from .models import Match
from chat.models import ChatRoom, Message, AutoCloseMessage, BadWordsLog  # ✅ 경로 수정

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'user1', 'user2', 'is_matched', 'matched_at')
    list_filter = ('is_matched',)
    search_fields = ('user1__email', 'user2__email')

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'match', 'created_at', 'is_active')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'sender', 'message_type', 'sent_at')
    search_fields = ('sender__email', 'content')

@admin.register(AutoCloseMessage)
class AutoCloseMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_default', 'content')

@admin.register(BadWordsLog)
class BadWordsLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'bad_word', 'filtered_at')
    search_fields = ('user__email', 'bad_word')
