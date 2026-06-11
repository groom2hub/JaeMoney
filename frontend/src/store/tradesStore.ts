import { create } from 'zustand';

interface Trade {
  id: number;
  symbol: string;
  company_name: string;
  trade_type: 'BUY' | 'SELL';
  quantity: number;
  price: number;
  total_amount: number;
  trade_date: string;
  disclosure_source?: string;
  created_at: string;
}

interface TradeStats {
  total_buy_amount: number;
  total_sell_amount: number;
  total_trades: number;
  buy_count: number;
  sell_count: number;
  net_amount: number;
}

interface TradesStore {
  trades: Trade[];
  stats: TradeStats | null;
  isLoading: boolean;
  setTrades: (trades: Trade[]) => void;
  setStats: (stats: TradeStats) => void;
  setLoading: (loading: boolean) => void;
  addTrade: (trade: Trade) => void;
}

export const useTradesStore = create<TradesStore>((set) => ({
  trades: [],
  stats: null,
  isLoading: false,
  setTrades: (trades) => set({ trades }),
  setStats: (stats) => set({ stats }),
  setLoading: (loading) => set({ isLoading: loading }),
  addTrade: (trade) =>
    set((state) => ({ trades: [trade, ...state.trades] })),
}));
