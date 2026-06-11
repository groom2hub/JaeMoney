import React, { useEffect } from 'react';
import {
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import StatCard from '../components/StatCard';
import { tradesAPI } from '../services/api';
import { useTradesStore } from '../store/tradesStore';

export default function Dashboard() {
  const { trades, stats, isLoading, setTrades, setStats, setLoading } =
    useTradesStore();

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        // ⭐ GitHub에서 JSON 다운로드
        const gitHubData = await tradesAPI.fetchFromGitHub();
        const tradesToDisplay = gitHubData.trades || [];
        setTrades(tradesToDisplay);

        // 통계 계산 (1회 순회)
        const calculatedStats = tradesToDisplay.reduce(
          (stats, t) => {
            const amount = t.total_amount || 0;
            return {
              total_buy_amount: t.trade_type === 'BUY' ? stats.total_buy_amount + amount : stats.total_buy_amount,
              total_sell_amount: t.trade_type === 'SELL' ? stats.total_sell_amount + amount : stats.total_sell_amount,
              total_trades: stats.total_trades + 1,
              buy_count: t.trade_type === 'BUY' ? stats.buy_count + 1 : stats.buy_count,
              sell_count: t.trade_type === 'SELL' ? stats.sell_count + 1 : stats.sell_count,
              net_amount: t.trade_type === 'BUY' ? stats.net_amount - amount : stats.net_amount + amount,
            };
          },
          {
            total_buy_amount: 0,
            total_sell_amount: 0,
            total_trades: 0,
            buy_count: 0,
            sell_count: 0,
            net_amount: 0,
          }
        );

        setStats(calculatedStats);
      } catch (error) {
        console.error('데이터 로드 실패:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [setTrades, setStats, setLoading]);

  const chartData = [
    { name: '매수', value: stats?.buy_count || 0 },
    { name: '매도', value: stats?.sell_count || 0 },
  ];

  const COLORS = ['#3b82f6', '#ef4444'];

  return (
    <div className="py-8">
      <h1 className="text-3xl font-bold mb-8">실시간 모니터링 대시보드</h1>

      {isLoading ? (
        <div className="text-center py-12">로딩 중...</div>
      ) : (
        <>
          {/* 통계 카드 */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <StatCard
              title="총 매수액"
              value={`${(stats?.total_buy_amount || 0).toLocaleString()}원`}
              icon="💰"
              color="blue"
            />
            <StatCard
              title="총 매도액"
              value={`${(stats?.total_sell_amount || 0).toLocaleString()}원`}
              icon="📈"
              color="green"
            />
            <StatCard
              title="총 거래 건수"
              value={stats?.total_trades || 0}
              icon="📊"
              color="yellow"
            />
            <StatCard
              title="순 자산"
              value={`${(stats?.net_amount || 0).toLocaleString()}원`}
              icon="💎"
              color={
                (stats?.net_amount || 0) >= 0 ? 'green' : 'red'
              }
            />
          </div>

          {/* 차트 */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            {/* 매수/매도 비율 */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-bold mb-4">매수/매도 비율</h2>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={chartData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, value }) => `${name}: ${value}`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>

            {/* 최근 거래 */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-bold mb-4">최근 거래</h2>
              <div className="space-y-3 max-h-80 overflow-y-auto">
                {trades.slice(0, 5).map((trade) => (
                  <div
                    key={trade.id}
                    className="flex justify-between items-center p-3 bg-gray-50 rounded"
                  >
                    <div>
                      <p className="font-semibold">{trade.company_name}</p>
                      <p className="text-sm text-gray-600">
                        {new Date(trade.trade_date).toLocaleDateString('ko-KR')}
                      </p>
                    </div>
                    <div className="text-right">
                      <p
                        className={`font-bold ${
                          trade.trade_type === 'BUY'
                            ? 'text-blue-600'
                            : 'text-red-600'
                        }`}
                      >
                        {trade.trade_type === 'BUY' ? '매수' : '매도'}
                      </p>
                      <p className="text-sm text-gray-600">
                        {trade.quantity.toLocaleString()}주
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
