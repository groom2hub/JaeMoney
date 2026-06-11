import React, { useEffect, useState } from 'react';
import { tradesAPI } from '../services/api';
import { useTradesStore } from '../store/tradesStore';

export default function TradeHistory() {
  const { trades, setTrades, isLoading, setLoading } = useTradesStore();
  const [filters, setFilters] = useState({
    symbol: '',
    trade_type: '',
  });

  useEffect(() => {
    const fetchTrades = async () => {
      setLoading(true);
      try {
        const res = await tradesAPI.getList(0, 100, filters);
        setTrades(res.data);
      } catch (error) {
        console.error('거래 정보 로드 실패:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTrades();
  }, [filters, setTrades, setLoading]);

  const handleFilterChange = (key: string, value: string) => {
    setFilters({ ...filters, [key]: value });
  };

  return (
    <div className="py-8">
      <h1 className="text-3xl font-bold mb-8">거래 히스토리</h1>

      {/* 필터 */}
      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <input
            type="text"
            placeholder="종목 검색..."
            value={filters.symbol}
            onChange={(e) => handleFilterChange('symbol', e.target.value)}
            className="border rounded px-3 py-2"
          />
          <select
            value={filters.trade_type}
            onChange={(e) => handleFilterChange('trade_type', e.target.value)}
            className="border rounded px-3 py-2"
          >
            <option value="">전체</option>
            <option value="BUY">매수</option>
            <option value="SELL">매도</option>
          </select>
        </div>
      </div>

      {/* 거래 목록 테이블 */}
      {isLoading ? (
        <div className="text-center py-12">로딩 중...</div>
      ) : (
        <div className="bg-white rounded-lg shadow overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-100 border-b">
              <tr>
                <th className="px-6 py-3 text-left">회사명</th>
                <th className="px-6 py-3 text-left">종목</th>
                <th className="px-6 py-3 text-left">유형</th>
                <th className="px-6 py-3 text-right">수량</th>
                <th className="px-6 py-3 text-right">주가</th>
                <th className="px-6 py-3 text-right">총액</th>
                <th className="px-6 py-3 text-left">날짜</th>
              </tr>
            </thead>
            <tbody>
              {trades.map((trade) => (
                <tr key={trade.id} className="border-b hover:bg-gray-50">
                  <td className="px-6 py-3">{trade.company_name}</td>
                  <td className="px-6 py-3">{trade.symbol}</td>
                  <td className="px-6 py-3">
                    <span
                      className={`px-3 py-1 rounded text-sm font-semibold ${
                        trade.trade_type === 'BUY'
                          ? 'bg-blue-100 text-blue-800'
                          : 'bg-red-100 text-red-800'
                      }`}
                    >
                      {trade.trade_type === 'BUY' ? '매수' : '매도'}
                    </span>
                  </td>
                  <td className="px-6 py-3 text-right">
                    {trade.quantity.toLocaleString()}
                  </td>
                  <td className="px-6 py-3 text-right">
                    {trade.price.toLocaleString()}원
                  </td>
                  <td className="px-6 py-3 text-right font-semibold">
                    {trade.total_amount.toLocaleString()}원
                  </td>
                  <td className="px-6 py-3">
                    {new Date(trade.trade_date).toLocaleDateString('ko-KR')}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {trades.length === 0 && (
            <div className="text-center py-12 text-gray-500">
              거래 기록이 없습니다.
            </div>
          )}
        </div>
      )}
    </div>
  );
}
