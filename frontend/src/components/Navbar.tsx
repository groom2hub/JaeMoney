import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

export default function Navbar() {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold text-blue-600">
          💰 JaeMoney
        </Link>

        <div className="flex gap-6">
          <Link to="/" className="hover:text-blue-600 transition">
            대시보드
          </Link>
          <Link to="/trades" className="hover:text-blue-600 transition">
            거래 히스토리
          </Link>
          <Link to="/profile" className="hover:text-blue-600 transition">
            프로필
          </Link>
        </div>

        <div className="flex items-center gap-4">
          <span className="text-gray-600">{user?.email}</span>
          <button
            onClick={handleLogout}
            className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded transition"
          >
            로그아웃
          </button>
        </div>
      </div>
    </nav>
  );
}
