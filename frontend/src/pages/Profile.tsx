import React, { useEffect, useState } from 'react';
import { subscriptionsAPI } from '../services/api';
import { useAuthStore } from '../store/authStore';

export default function Profile() {
  const { user } = useAuthStore();
  const [subscriptions, setSubscriptions] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchSubscriptions = async () => {
      setLoading(true);
      try {
        const res = await subscriptionsAPI.getList();
        setSubscriptions(res.data);
      } catch (error) {
        console.error('구독 정보 로드 실패:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchSubscriptions();
  }, []);

  const handleToggle = async (id: number) => {
    try {
      await subscriptionsAPI.toggle(id);
      const res = await subscriptionsAPI.getList();
      setSubscriptions(res.data);
    } catch (error) {
      console.error('구독 토글 실패:', error);
    }
  };

  const channelLabel: Record<string, string> = {
    EMAIL: '이메일',
    SMS: 'SMS',
    KAKAO_TALK: '카카오톡',
  };

  return (
    <div className="py-8">
      <h1 className="text-3xl font-bold mb-8">프로필</h1>

      {/* 사용자 정보 */}
      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <h2 className="text-xl font-bold mb-4">계정 정보</h2>
        <div className="space-y-2">
          <p className="text-gray-600">
            <span className="font-semibold">이메일:</span> {user?.email}
          </p>
          <p className="text-gray-600">
            <span className="font-semibold">전화번호:</span>{' '}
            {user?.phone_number || '등록되지 않음'}
          </p>
        </div>
      </div>

      {/* 알림 구독 설정 */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold mb-4">알림 구독 설정</h2>

        {loading ? (
          <div className="text-center py-8">로딩 중...</div>
        ) : (
          <div className="space-y-4">
            {subscriptions.length > 0 ? (
              subscriptions.map((sub: any) => (
                <div
                  key={sub.id}
                  className="flex items-center justify-between p-4 bg-gray-50 rounded"
                >
                  <div>
                    <p className="font-semibold">
                      {channelLabel[sub.channel]}
                    </p>
                    <p className="text-sm text-gray-600">
                      {sub.start_time} ~ {sub.end_time}
                    </p>
                  </div>
                  <button
                    onClick={() => handleToggle(sub.id)}
                    className={`px-4 py-2 rounded font-semibold transition ${
                      sub.is_active
                        ? 'bg-green-500 hover:bg-green-600 text-white'
                        : 'bg-gray-300 hover:bg-gray-400 text-gray-700'
                    }`}
                  >
                    {sub.is_active ? '구독 중' : '구독 안 함'}
                  </button>
                </div>
              ))
            ) : (
              <div className="text-center py-8 text-gray-500">
                구독한 채널이 없습니다.
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
