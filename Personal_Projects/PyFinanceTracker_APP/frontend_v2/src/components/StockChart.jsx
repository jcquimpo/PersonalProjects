/**
 * StockChart Component - Displays OHLC chart for a stock.
 */

import React from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import '../styles/StockChart.css';

const StockChart = ({ data, symbol, company_name }) => {
  if (!data || data.length === 0) {
    return (
      <div className="stock-chart-container">
        <div className="chart-placeholder">
          <p>No data available for {symbol}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="stock-chart-container">
      <div className="chart-header">
        <h2>{symbol}</h2>
        <p className="chart-company-name">{company_name}</p>
      </div>

      <div className="chart-wrapper">
        <div className="chart-section">
          <h3>Closing Price Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis
                dataKey="date"
                stroke="#9ca3af"
                style={{ fontSize: '12px' }}
              />
              <YAxis stroke="#9ca3af" style={{ fontSize: '12px' }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1f2937',
                  border: '1px solid #374151',
                  borderRadius: '8px',
                  color: '#f3f4f6',
                }}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="close"
                stroke="#3b82f6"
                dot={{ r: 4 }}
                activeDot={{ r: 6 }}
                strokeWidth={2}
                name="Close"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-section">
          <h3>OHLC Data</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis
                dataKey="date"
                stroke="#9ca3af"
                style={{ fontSize: '12px' }}
              />
              <YAxis stroke="#9ca3af" style={{ fontSize: '12px' }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1f2937',
                  border: '1px solid #374151',
                  borderRadius: '8px',
                  color: '#f3f4f6',
                }}
              />
              <Legend />
              <Bar dataKey="open" stackId="a" fill="#8b5cf6" name="Open" />
              <Bar dataKey="high" stackId="a" fill="#10b981" name="High" />
              <Bar dataKey="low" stackId="a" fill="#ef4444" name="Low" />
              <Bar dataKey="close" stackId="a" fill="#3b82f6" name="Close" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default StockChart;
