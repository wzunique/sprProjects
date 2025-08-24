#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MEGA彩票号码规律分析工具
分析最近十期的开奖号码，寻找可能的规律和趋势
"""

import requests
import json
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

class MegaLotteryAnalyzer:
    def __init__(self):
        self.base_url = "https://api.opap.gr/draws/v3.0/1100"
        self.recent_draws = []
        
    def fetch_recent_draws(self, count=10):
        """获取最近的开奖结果"""
        try:
            # 尝试从OPAP API获取数据
            response = requests.get(f"{self.base_url}/draws", params={
                'limit': count,
                'status': 'DRAW'
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.recent_draws = data.get('content', [])
                return True
            else:
                print(f"API请求失败，状态码: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"获取数据时出错: {e}")
            return False
    
    def generate_sample_data(self):
        """生成示例数据用于演示"""
        print("使用示例数据进行演示分析...")
        
        # 模拟最近10期MEGA彩票开奖号码
        sample_draws = [
            {"drawId": 1001, "winningNumbers": {"list": [3, 12, 25, 38, 45]}, "bonus": [7], "drawTime": "2024-01-15T20:00:00"},
            {"drawId": 1002, "winningNumbers": {"list": [8, 19, 27, 33, 41]}, "bonus": [12], "drawTime": "2024-01-16T20:00:00"},
            {"drawId": 1003, "winningNumbers": {"list": [5, 16, 22, 35, 44]}, "bonus": [9], "drawTime": "2024-01-17T20:00:00"},
            {"drawId": 1004, "winningNumbers": {"list": [11, 18, 29, 36, 42]}, "bonus": [6], "drawTime": "2024-01-18T20:00:00"},
            {"drawId": 1005, "winningNumbers": {"list": [2, 14, 23, 31, 39]}, "bonus": [15], "drawTime": "2024-01-19T20:00:00"},
            {"drawId": 1006, "winningNumbers": {"list": [7, 17, 26, 34, 43]}, "bonus": [11], "drawTime": "2024-01-20T20:00:00"},
            {"drawId": 1007, "winningNumbers": {"list": [9, 20, 28, 37, 46]}, "bonus": [4], "drawTime": "2024-01-21T20:00:00"},
            {"drawId": 1008, "winningNumbers": {"list": [4, 13, 21, 32, 40]}, "bonus": [8], "drawTime": "2024-01-22T20:00:00"},
            {"drawId": 1009, "winningNumbers": {"list": [6, 15, 24, 30, 38]}, "bonus": [13], "drawTime": "2024-01-23T20:00:00"},
            {"drawId": 1010, "winningNumbers": {"list": [10, 19, 25, 33, 41]}, "bonus": [5], "drawTime": "2024-01-24T20:00:00"}
        ]
        
        self.recent_draws = sample_draws
        return True
    
    def analyze_number_frequency(self):
        """分析号码出现频率"""
        if not self.recent_draws:
            print("没有数据可供分析")
            return None
            
        all_numbers = []
        bonus_numbers = []
        
        for draw in self.recent_draws:
            numbers = draw.get('winningNumbers', {}).get('list', [])
            bonus = draw.get('bonus', [])
            all_numbers.extend(numbers)
            bonus_numbers.extend(bonus)
        
        # 统计主号码频率
        main_freq = Counter(all_numbers)
        bonus_freq = Counter(bonus_numbers)
        
        return main_freq, bonus_freq
    
    def analyze_number_patterns(self):
        """分析号码模式"""
        if not self.recent_draws:
            return None
            
        patterns = {
            'odd_even_ratio': [],
            'high_low_ratio': [],
            'sum_range': [],
            'consecutive_numbers': [],
            'number_gaps': []
        }
        
        for draw in self.recent_draws:
            numbers = sorted(draw.get('winningNumbers', {}).get('list', []))
            
            # 奇偶比例
            odd_count = len([n for n in numbers if n % 2 == 1])
            even_count = len([n for n in numbers if n % 2 == 0])
            patterns['odd_even_ratio'].append(f"{odd_count}:{even_count}")
            
            # 大小比例 (1-25为小，26-50为大)
            low_count = len([n for n in numbers if n <= 25])
            high_count = len([n for n in numbers if n > 25])
            patterns['high_low_ratio'].append(f"{low_count}:{high_count}")
            
            # 号码和值范围
            sum_value = sum(numbers)
            patterns['sum_range'].append(sum_value)
            
            # 连续号码
            consecutive = 0
            for i in range(len(numbers)-1):
                if numbers[i+1] - numbers[i] == 1:
                    consecutive += 1
            patterns['consecutive_numbers'].append(consecutive)
            
            # 号码间隔
            gaps = [numbers[i+1] - numbers[i] for i in range(len(numbers)-1)]
            patterns['number_gaps'].append(gaps)
        
        return patterns
    
    def find_hot_cold_numbers(self, main_freq):
        """找出热号和冷号"""
        if not main_freq:
            return None
            
        # 按频率排序
        sorted_freq = sorted(main_freq.items(), key=lambda x: x[1], reverse=True)
        
        hot_numbers = sorted_freq[:5]  # 前5个最热号码
        cold_numbers = sorted_freq[-5:]  # 后5个最冷号码
        
        return hot_numbers, cold_numbers
    
    def generate_statistics_report(self):
        """生成统计报告"""
        if not self.recent_draws:
            print("没有数据可供分析")
            return
            
        print("=" * 60)
        print("MEGA彩票最近十期号码规律分析报告")
        print("=" * 60)
        print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"分析期数: {len(self.recent_draws)}期")
        print()
        
        # 显示最近十期开奖号码
        print("最近十期开奖号码:")
        print("-" * 40)
        for i, draw in enumerate(self.recent_draws, 1):
            numbers = draw.get('winningNumbers', {}).get('list', [])
            bonus = draw.get('bonus', [])
            print(f"第{draw.get('drawId', i)}期: {sorted(numbers)} + 特别号{bonus}")
        print()
        
        # 号码频率分析
        main_freq, bonus_freq = self.analyze_number_frequency()
        if main_freq:
            print("主号码出现频率:")
            print("-" * 30)
            for num, freq in sorted(main_freq.items()):
                print(f"号码{num:2d}: {freq}次")
            print()
            
            # 热号和冷号
            hot_numbers, cold_numbers = self.find_hot_cold_numbers(main_freq)
            print("热号 (出现频率最高):")
            for num, freq in hot_numbers:
                print(f"  号码{num}: {freq}次")
            print()
            
            print("冷号 (出现频率最低):")
            for num, freq in cold_numbers:
                print(f"  号码{num}: {freq}次")
            print()
        
        # 特别号分析
        if bonus_freq:
            print("特别号出现频率:")
            print("-" * 30)
            for num, freq in sorted(bonus_freq.items()):
                print(f"特别号{num:2d}: {freq}次")
            print()
        
        # 模式分析
        patterns = self.analyze_number_patterns()
        if patterns:
            print("号码模式分析:")
            print("-" * 30)
            
            # 奇偶比例
            odd_even_counts = Counter(patterns['odd_even_ratio'])
            print("奇偶比例分布:")
            for ratio, count in odd_even_counts.most_common():
                print(f"  {ratio}: {count}次")
            print()
            
            # 大小比例
            high_low_counts = Counter(patterns['high_low_ratio'])
            print("大小比例分布:")
            for ratio, count in high_low_counts.most_common():
                print(f"  {ratio}: {count}次")
            print()
            
            # 和值范围
            sum_values = patterns['sum_range']
            print(f"号码和值范围: {min(sum_values)} - {max(sum_values)}")
            print(f"平均和值: {np.mean(sum_values):.1f}")
            print(f"和值中位数: {np.median(sum_values):.1f}")
            print()
            
            # 连续号码
            consecutive_counts = Counter(patterns['consecutive_numbers'])
            print("连续号码分布:")
            for count, freq in sorted(consecutive_counts.items()):
                print(f"  {count}个连续号码: {freq}次")
            print()
    
    def create_visualizations(self):
        """创建可视化图表"""
        if not self.recent_draws:
            print("没有数据可供可视化")
            return
            
        main_freq, bonus_freq = self.analyze_number_frequency()
        if not main_freq:
            return
            
        # 创建图表
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('MEGA彩票号码规律分析图表', fontsize=16, fontweight='bold')
        
        # 1. 主号码频率柱状图
        numbers = list(main_freq.keys())
        frequencies = list(main_freq.values())
        
        axes[0, 0].bar(numbers, frequencies, color='skyblue', alpha=0.7)
        axes[0, 0].set_title('主号码出现频率')
        axes[0, 0].set_xlabel('号码')
        axes[0, 0].set_ylabel('出现次数')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. 特别号频率饼图
        if bonus_freq:
            bonus_nums = list(bonus_freq.keys())
            bonus_freqs = list(bonus_freq.values())
            axes[0, 1].pie(bonus_freqs, labels=bonus_nums, autopct='%1.1f%%', startangle=90)
            axes[0, 1].set_title('特别号出现频率')
        
        # 3. 号码和值趋势
        patterns = self.analyze_number_patterns()
        if patterns and patterns['sum_range']:
            draw_ids = [f"第{i+1}期" for i in range(len(patterns['sum_range']))]
            axes[1, 0].plot(draw_ids, patterns['sum_range'], marker='o', linewidth=2, markersize=8)
            axes[1, 0].set_title('号码和值趋势')
            axes[1, 0].set_xlabel('期数')
            axes[1, 0].set_ylabel('和值')
            axes[1, 0].grid(True, alpha=0.3)
            axes[1, 0].tick_params(axis='x', rotation=45)
        
        # 4. 奇偶比例分布
        if patterns and patterns['odd_even_ratio']:
            odd_even_counts = Counter(patterns['odd_even_ratio'])
            ratios = list(odd_even_counts.keys())
            counts = list(odd_even_counts.values())
            
            axes[1, 1].bar(range(len(ratios)), counts, color='lightcoral', alpha=0.7)
            axes[1, 1].set_title('奇偶比例分布')
            axes[1, 1].set_xlabel('奇偶比例')
            axes[1, 1].set_ylabel('出现次数')
            axes[1, 1].set_xticks(range(len(ratios)))
            axes[1, 1].set_xticklabels(ratios)
            axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('mega_lottery_analysis.png', dpi=300, bbox_inches='tight')
        print("图表已保存为 'mega_lottery_analysis.png'")
        plt.show()
    
    def predict_trends(self):
        """预测趋势和建议"""
        print("=" * 60)
        print("趋势预测和投注建议")
        print("=" * 60)
        
        if not self.recent_draws:
            print("数据不足，无法进行趋势预测")
            return
            
        main_freq, bonus_freq = self.analyze_number_frequency()
        patterns = self.analyze_number_patterns()
        
        if not main_freq or not patterns:
            return
            
        print("基于历史数据的趋势分析:")
        print("-" * 40)
        
        # 分析奇偶趋势
        odd_even_counts = Counter(patterns['odd_even_ratio'])
        most_common_odd_even = odd_even_counts.most_common(1)[0]
        print(f"最常见的奇偶比例: {most_common_odd_even[0]} (出现{most_common_odd_even[1]}次)")
        
        # 分析大小趋势
        high_low_counts = Counter(patterns['high_low_ratio'])
        most_common_high_low = high_low_counts.most_common(1)[0]
        print(f"最常见的大小比例: {most_common_high_low[0]} (出现{most_common_high_low[1]}次)")
        
        # 分析号码和值趋势
        sum_values = patterns['sum_range']
        avg_sum = np.mean(sum_values)
        print(f"平均号码和值: {avg_sum:.1f}")
        
        # 投注建议
        print("\n投注建议:")
        print("-" * 20)
        
        # 基于频率的建议
        hot_numbers, cold_numbers = self.find_hot_cold_numbers(main_freq)
        print("建议关注的热号:")
        for num, freq in hot_numbers[:3]:
            print(f"  号码{num} (出现{freq}次)")
        
        print("\n建议关注的冷号:")
        for num, freq in cold_numbers[:3]:
            print(f"  号码{num} (出现{freq}次)")
        
        # 基于模式的建议
        print(f"\n建议号码和值范围: {int(avg_sum-10)} - {int(avg_sum+10)}")
        
        # 风险提示
        print("\n⚠️  重要提醒:")
        print("1. 彩票具有随机性，历史数据仅供参考")
        print("2. 请理性投注，不要超出承受能力")
        print("3. 本分析工具仅供娱乐和学习使用")
        print("4. 实际投注请以官方开奖结果为准")

def main():
    """主函数"""
    print("MEGA彩票号码规律分析工具")
    print("=" * 50)
    
    analyzer = MegaLotteryAnalyzer()
    
    # 尝试获取真实数据，如果失败则使用示例数据
    if not analyzer.fetch_recent_draws():
        print("无法获取真实数据，使用示例数据进行演示...")
        analyzer.generate_sample_data()
    
    # 生成分析报告
    analyzer.generate_statistics_report()
    
    # 创建可视化图表
    print("\n正在生成可视化图表...")
    analyzer.create_visualizations()
    
    # 预测趋势和建议
    analyzer.predict_trends()
    
    print("\n分析完成！")

if __name__ == "__main__":
    main()

