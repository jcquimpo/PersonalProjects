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
  ComposedChart
} from 'recharts';
import '../styles/StockChart.css';

function StockChart({ data, symbol }) {
  if (!data || data.length === 0) {
    return <div className="chart-placeholder">No data available</div>;
  }

  // Prepare data for charts
  const chartData = data.map(d => ({
    date: d.date.slice(5), // MM-DD format
    open: d.open,
    high: d.high,
    low: d.low,
    close: d.close
  }));

  return (
    <div className="chart-section">
      <div className="chart-wrapper">
        <h3>OHLC Trend (7-Day)</h3>
        <ResponsiveContainer width="100%" height={400}>
          <ComposedChart data={chartData} margin={{ top: 5, right: 30, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
            <XAxis dataKey="date" stroke="#666" />
            <YAxis stroke="#666" />
            <Tooltip 
              contentStyle={{ backgroundColor: '#fff', border: '1px solid #ccc' }}
              formatter={(value) => `$${value.toFixed(2)}`}
            />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="open" 
              stroke="#3b82f6" 
              strokeWidth={2}
              name="Open"
              dot={{ r: 4 }}
            />
            <Line 
              type="monotone" 
              dataKey="high" 
              stroke="#10b981" 
              strokeWidth={2}
              name="High"
              dot={{ r: 4 }}
            />
            <Line 
              type="monotone" 
              dataKey="low" 
              stroke="#ef4444" 
              strokeWidth={2}
              name="Low"
              dot={{ r: 4 }}
            />
            <Line 
              type="monotone" 
              dataKey="close" 
              stroke="#8b5cf6" 
              strokeWidth={3}
              name="Close"
              dot={{ r: 5 }}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>

      <div className="chart-wrapper">
        <h3>Closing Price Range</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData} margin={{ top: 5, right: 30, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
            <XAxis dataKey="date" stroke="#666" />
            <YAxis stroke="#666" />
            <Tooltip 
              contentStyle={{ backgroundColor: '#fff', border: '1px solid #ccc' }}
              formatter={(value) => `$${value.toFixed(2)}`}
            />
            <Bar dataKey="close" fill="#8b5cf6" name="Close" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="chart-stats">
        <div className="stat-box">
          <label>Highest</label>
          <value className="high-val">
            ${Math.max(...chartData.map(d => d.high)).toFixed(2)}
          </value>
        </div>
        <div className="stat-box">
          <label>Lowest</label>
          <value className="low-val">
            ${Math.min(...chartData.map(d => d.low)).toFixed(2)}
          </value>
        </div>
        <div className="stat-box">
          <label>Average Close</label>
          <value className="avg-val">
            ${(chartData.reduce((sum, d) => sum + d.close, 0) / chartData.length).toFixed(2)}
          </value>
        </div>
      </div>
    </div>
  );
}

export default StockChart;
