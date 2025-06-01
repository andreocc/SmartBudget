#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SmartBudget - Dashboard Financeiro Inteligente
Análise avançada de gastos com IA preditiva para extratos do Nubank
Autor: Andre Occenstein
Versão: 1.0
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime, timedelta
import re
from collections import defaultdict
import os
import locale

# Configurar locale para formato brasileiro
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
    except:
        pass

class SmartBudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SmartBudget - Dashboard Financeiro Inteligente")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a1a')
        self.root.resizable(True, True)
        
        # Dados da aplicação
        self.df = None
        self.categorias_personalizadas = {}
        
        # Configurar estilo
        self.setup_style()
        
        # Criar interface
        self.create_main_interface()
        
        # Dados de exemplo para demonstração
        self.create_sample_data()
    
    def setup_style(self):
        """Configurar tema escuro moderno"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Cores do tema
        bg_color = '#1a1a1a'
        fg_color = '#ffffff'
        select_bg = '#404040'
        
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color, font=('Segoe UI', 10))
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'))
        style.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'))
        style.configure('TButton', font=('Segoe UI', 10))
        
        # Configurar matplotlib para tema escuro
        plt.style.use('dark_background')
    
    def create_main_interface(self):
        """Criar interface principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header com título e botão de importação
        self.create_header(main_frame)
        
        # Frame de conteúdo principal
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Painel esquerdo - Métricas e Score
        left_panel = ttk.Frame(content_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Painel direito - Gráficos
        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Criar seções
        self.create_metrics_section(left_panel)
        self.create_charts_section(right_panel)
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """Criar cabeçalho da aplicação"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Título
        title_label = ttk.Label(header_frame, text="💰 SmartBudget", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Subtítulo
        subtitle_label = ttk.Label(header_frame, text="Dashboard Financeiro Inteligente", 
                                 font=('Segoe UI', 10, 'italic'))
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Botão de importar
        import_btn = ttk.Button(header_frame, text="📁 Importar CSV Nubank", 
                               command=self.import_csv)
        import_btn.pack(side=tk.RIGHT)
        
        # Botão de dados de exemplo
        sample_btn = ttk.Button(header_frame, text="🎯 Usar Dados Exemplo", 
                               command=self.load_sample_data)
        sample_btn.pack(side=tk.RIGHT, padx=(0, 10))
    
    def create_metrics_section(self, parent):
        """Criar seção de métricas e score"""
        # Score de Saúde Financeira
        score_frame = tk.Frame(parent, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        score_frame.pack(fill=tk.X, pady=(0, 10))
        
        score_title = tk.Label(score_frame, text="🎯 Score de Saúde Financeira", 
                              bg='#2d2d2d', fg='white', font=('Segoe UI', 12, 'bold'))
        score_title.pack(pady=5)
        
        self.score_label = tk.Label(score_frame, text="--", 
                                   bg='#2d2d2d', fg='#00ff00', font=('Segoe UI', 24, 'bold'))
        self.score_label.pack(pady=5)
        
        self.score_desc = tk.Label(score_frame, text="Aguardando dados...", 
                                  bg='#2d2d2d', fg='#cccccc', font=('Segoe UI', 10))
        self.score_desc.pack(pady=(0, 10))
        
        # Métricas principais
        metrics_frame = tk.Frame(parent, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        metrics_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        metrics_title = tk.Label(metrics_frame, text="📊 Métricas do Mês", 
                                bg='#2d2d2d', fg='white', font=('Segoe UI', 12, 'bold'))
        metrics_title.pack(pady=5)
        
        # Frame para métricas
        self.metrics_content = tk.Frame(metrics_frame, bg='#2d2d2d')
        self.metrics_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Previsões e Alertas
        predictions_frame = tk.Frame(parent, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        predictions_frame.pack(fill=tk.X)
        
        pred_title = tk.Label(predictions_frame, text="🔮 Previsões e Alertas", 
                             bg='#2d2d2d', fg='white', font=('Segoe UI', 12, 'bold'))
        pred_title.pack(pady=5)
        
        self.predictions_content = tk.Frame(predictions_frame, bg='#2d2d2d')
        self.predictions_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def create_charts_section(self, parent):
        """Criar seção de gráficos"""
        # Notebook para múltiplos gráficos
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Aba 1: Evolução Mensal
        evolution_frame = ttk.Frame(notebook)
        notebook.add(evolution_frame, text="📈 Evolução Mensal")
        
        # Aba 2: Categorias
        categories_frame = ttk.Frame(notebook)
        notebook.add(categories_frame, text="🏷️ Por Categoria")
        
        # Aba 3: Padrões
        patterns_frame = ttk.Frame(notebook)
        notebook.add(patterns_frame, text="🔍 Padrões")
        
        # Criar canvas para gráficos
        self.create_evolution_chart(evolution_frame)
        self.create_categories_chart(categories_frame)
        self.create_patterns_chart(patterns_frame)
    
    def create_evolution_chart(self, parent):
        """Criar gráfico de evolução mensal"""
        fig = Figure(figsize=(8, 6), facecolor='#1a1a1a')
        self.evolution_ax = fig.add_subplot(111, facecolor='#2d2d2d')
        
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.evolution_canvas = canvas
    
    def create_categories_chart(self, parent):
        """Criar gráfico de categorias"""
        fig = Figure(figsize=(8, 6), facecolor='#1a1a1a')
        self.categories_ax = fig.add_subplot(111, facecolor='#2d2d2d')
        
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.categories_canvas = canvas
    
    def create_patterns_chart(self, parent):
        """Criar gráfico de padrões"""
        fig = Figure(figsize=(8, 6), facecolor='#1a1a1a')
        self.patterns_ax = fig.add_subplot(111, facecolor='#2d2d2d')
        
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.patterns_canvas = canvas
    
    def create_status_bar(self, parent):
        """Criar barra de status"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="Pronto para analisar seus dados financeiros")
        self.status_label.pack(side=tk.LEFT)
        
        # Info da versão
        version_label = ttk.Label(status_frame, text="SmartBudget v1.0")
        version_label.pack(side=tk.RIGHT)
    
    def create_sample_data(self):
        """Criar dados de exemplo para demonstração"""
        # Gerar dados realistas dos últimos 6 meses
        dates = []
        values = []
        descriptions = []
        
        base_date = datetime.now() - timedelta(days=180)
        
        # Categorias e gastos típicos
        expenses = {
            'Alimentação': ['IFOOD', 'UBER EATS', 'RESTAURANTE', 'SUPERMERCADO', 'PADARIA'],
            'Transporte': ['UBER', '99', 'POSTO', 'ESTACIONAMENTO'],
            'Entretenimento': ['NETFLIX', 'SPOTIFY', 'CINEMA', 'SHOPPING'],
            'Saúde': ['FARMACIA', 'CONSULTA', 'PLANO SAUDE'],
            'Casa': ['MERCADO', 'LIMPEZA', 'CONTA LUZ', 'CONTA AGUA'],
            'Educação': ['CURSO', 'LIVRO', 'ESCOLA']
        }
        
        for i in range(300):  # 300 transações
            date = base_date + timedelta(days=np.random.randint(0, 180))
            
            category = np.random.choice(list(expenses.keys()))
            desc_base = np.random.choice(expenses[category])
            
            # Valores mais realistas por categoria
            if category == 'Alimentação':
                value = -np.random.uniform(15, 150)
            elif category == 'Transporte':
                value = -np.random.uniform(8, 80)
            elif category == 'Entretenimento':
                value = -np.random.uniform(10, 200)
            elif category == 'Saúde':
                value = -np.random.uniform(20, 300)
            elif category == 'Casa':
                value = -np.random.uniform(30, 400)
            else:
                value = -np.random.uniform(25, 250)
            
            dates.append(date.strftime('%Y-%m-%d'))
            values.append(round(value, 2))
            descriptions.append(f"{desc_base} *{np.random.randint(1000, 9999)}")
        
        # Adicionar algumas receitas
        for i in range(12):  # Salários mensais
            date = base_date + timedelta(days=i*15)
            dates.append(date.strftime('%Y-%m-%d'))
            values.append(3500.00)  # Salário
            descriptions.append("SALARIO EMPRESA")
        
        self.sample_df = pd.DataFrame({
            'Data': dates,
            'Valor': values,
            'Descrição': descriptions
        })
    
    def load_sample_data(self):
        """Carregar dados de exemplo"""
        self.df = self.sample_df.copy()
        self.process_data()
        self.status_label.config(text="Dados de exemplo carregados com sucesso!")
    
    def import_csv(self):
        """Importar arquivo CSV do Nubank"""
        file_path = filedialog.askopenfilename(
            title="Selecione o arquivo CSV do Nubank",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            # Tentar diferentes encodings
            encodings = ['utf-8', 'latin-1', 'cp1252']
            df = None
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                raise Exception("Não foi possível ler o arquivo com nenhuma codificação")
            
            # Detectar formato do Nubank
            df = self.detect_nubank_format(df)
            
            if df is not None:
                self.df = df
                self.process_data()
                self.status_label.config(text=f"Arquivo importado: {len(df)} transações processadas")
            else:
                messagebox.showerror("Erro", "Formato do arquivo não reconhecido como CSV do Nubank")
                
        except Exception as e:
            messagebox.showerror("Erro ao importar", f"Erro: {str(e)}")
    
    def detect_nubank_format(self, df):
        """Detectar e padronizar formato do CSV do Nubank"""
        # Mapear possíveis nomes de colunas
        column_mapping = {
            'data': ['Data', 'date', 'Data da transação'],
            'valor': ['Valor', 'value', 'Valor da transação', 'amount'],
            'descricao': ['Descrição', 'description', 'Estabelecimento', 'merchant']
        }
        
        # Detectar colunas
        detected_columns = {}
        
        for key, possible_names in column_mapping.items():
            for col in df.columns:
                if any(name.lower() in col.lower() for name in possible_names):
                    detected_columns[key] = col
                    break
        
        if len(detected_columns) < 3:
            return None
        
        # Criar DataFrame padronizado
        standardized_df = pd.DataFrame()
        standardized_df['Data'] = df[detected_columns['data']]
        standardized_df['Valor'] = df[detected_columns['valor']]
        standardized_df['Descrição'] = df[detected_columns['descricao']]
        
        # Limpar e converter dados
        standardized_df['Data'] = pd.to_datetime(standardized_df['Data'], errors='coerce')
        standardized_df['Valor'] = pd.to_numeric(standardized_df['Valor'], errors='coerce')
        standardized_df = standardized_df.dropna()
        
        return standardized_df
    
    def categorize_transaction(self, description):
        """Categorizar transação baseada na descrição"""
        description = description.upper()
        
        categories = {
            'Alimentação': ['IFOOD', 'UBER EATS', 'RESTAURANTE', 'SUPERMERCADO', 'PADARIA', 'LANCHONETE', 'PIZZA', 'MCDONALDS', 'BK', 'SUBWAY'],
            'Transporte': ['UBER', '99', 'POSTO', 'COMBUSTIVEL', 'ESTACIONAMENTO', 'PEDÁGIO', 'ONIBUS', 'METRO'],
            'Entretenimento': ['NETFLIX', 'SPOTIFY', 'CINEMA', 'SHOPPING', 'TEATRO', 'SHOW', 'PARQUE', 'INGRESSO'],
            'Saúde': ['FARMACIA', 'DROGARIA', 'CONSULTA', 'HOSPITAL', 'CLINICA', 'PLANO', 'MEDICO', 'DENTISTA'],
            'Casa': ['MERCADO', 'LIMPEZA', 'LUZ', 'AGUA', 'GAS', 'INTERNET', 'TELEFONE', 'CONDOMINIO'],
            'Educação': ['CURSO', 'LIVRO', 'ESCOLA', 'FACULDADE', 'UNIVERSIDADE', 'APOSTILA'],
            'Vestuário': ['ROUPA', 'SAPATO', 'LOJA', 'CALCADO', 'MODA'],
            'Tecnologia': ['APPLE', 'SAMSUNG', 'INFORMATICA', 'ELETRONICOS', 'CELULAR'],
            'Receita': ['SALARIO', 'PIX RECEBIDO', 'TRANSFERENCIA RECEBIDA', 'RENDIMENTO']
        }
        
        for category, keywords in categories.items():
            if any(keyword in description for keyword in keywords):
                return category
        
        return 'Outros'
    
    def calculate_financial_score(self):
        """Calcular score de saúde financeira"""
        if self.df is None or len(self.df) == 0:
            return 0, "Sem dados"
        
        # Últimos 30 dias
        last_month = self.df[self.df['Data'] >= datetime.now() - timedelta(days=30)]
        
        if len(last_month) == 0:
            return 0, "Dados insuficientes"
        
        score = 100
        
        # Fator 1: Proporção receita/despesa
        receitas = last_month[last_month['Valor'] > 0]['Valor'].sum()
        despesas = abs(last_month[last_month['Valor'] < 0]['Valor'].sum())
        
        if receitas > 0:
            ratio = despesas / receitas
            if ratio > 1:  # Gastando mais que ganha
                score -= 40
            elif ratio > 0.8:  # Gastando mais de 80%
                score -= 20
        else:
            score -= 30
        
        # Fator 2: Variabilidade dos gastos
        daily_expenses = last_month[last_month['Valor'] < 0].groupby(last_month['Data'].dt.date)['Valor'].sum()
        if len(daily_expenses) > 1:
            cv = daily_expenses.std() / abs(daily_expenses.mean())
            if cv > 1:  # Muito irregular
                score -= 15
        
        # Fator 3: Gastos por categoria
        categories = last_month.apply(lambda x: self.categorize_transaction(x['Descrição']), axis=1)
        category_spending = last_month.groupby(categories)['Valor'].sum()
        
        alimentacao_pct = abs(category_spending.get('Alimentação', 0)) / despesas if despesas > 0 else 0
        if alimentacao_pct > 0.4:  # Mais de 40% em comida
            score -= 10
        
        score = max(0, min(100, score))
        
        # Descrição do score
        if score >= 80:
            desc = "Excelente! Finanças muito saudáveis"
        elif score >= 60:
            desc = "Bom! Algumas melhorias possíveis"
        elif score >= 40:
            desc = "Atenção! Precisa de ajustes"
        else:
            desc = "Crítico! Reavalie seus gastos"
        
        return int(score), desc
    
    def predict_next_month(self):
        """Prever gastos do próximo mês"""
        if self.df is None or len(self.df) == 0:
            return 0
        
        # Últimos 3 meses de dados
        last_3_months = self.df[self.df['Data'] >= datetime.now() - timedelta(days=90)]
        
        if len(last_3_months) == 0:
            return 0
        
        # Média mensal de gastos
        monthly_expenses = last_3_months[last_3_months['Valor'] < 0].groupby(
            last_3_months['Data'].dt.to_period('M')
        )['Valor'].sum()
        
        if len(monthly_expenses) == 0:
            return 0
        
        # Tendência (regressão linear simples)
        if len(monthly_expenses) > 1:
            x = np.arange(len(monthly_expenses))
            y = monthly_expenses.values
            trend = np.polyfit(x, y, 1)[0]
            prediction = monthly_expenses.iloc[-1] + trend
        else:
            prediction = monthly_expenses.iloc[0]
        
        return abs(prediction)
    
    def process_data(self):
        """Processar dados e atualizar interface"""
        if self.df is None:
            return
        
        # Adicionar categorias
        self.df['Categoria'] = self.df.apply(lambda x: self.categorize_transaction(x['Descrição']), axis=1)
        
        # Atualizar métricas
        self.update_metrics()
        
        # Atualizar gráficos
        self.update_charts()
    
    def update_metrics(self):
        """Atualizar métricas na interface"""
        # Limpar conteúdo anterior
        for widget in self.metrics_content.winfo_children():
            widget.destroy()
        for widget in self.predictions_content.winfo_children():
            widget.destroy()
        
        if self.df is None:
            return
        
        # Calcular score
        score, score_desc = self.calculate_financial_score()
        self.score_label.config(text=f"{score}")
        self.score_desc.config(text=score_desc)
        
        # Cor do score
        if score >= 80:
            color = '#00ff00'
        elif score >= 60:
            color = '#ffff00'
        elif score >= 40:
            color = '#ff8800'
        else:
            color = '#ff0000'
        self.score_label.config(fg=color)
        
        # Métricas do mês atual
        current_month = self.df[self.df['Data'].dt.month == datetime.now().month]
        
        if len(current_month) > 0:
            receitas = current_month[current_month['Valor'] > 0]['Valor'].sum()
            despesas = abs(current_month[current_month['Valor'] < 0]['Valor'].sum())
            saldo = receitas - despesas
            
            # Exibir métricas
            metrics = [
                ("💰 Receitas", f"R$ {receitas:,.2f}", '#00ff00'),
                ("💸 Despesas", f"R$ {despesas:,.2f}", '#ff4444'),
                ("💳 Saldo", f"R$ {saldo:,.2f}", '#00ff00' if saldo >= 0 else '#ff4444'),
                ("📊 Transações", f"{len(current_month)}", '#888888')
            ]
            
            for i, (label, value, color) in enumerate(metrics):
                row = i // 2
                col = i % 2
                
                metric_frame = tk.Frame(self.metrics_content, bg='#404040', relief=tk.RAISED, bd=1)
                metric_frame.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
                
                tk.Label(metric_frame, text=label, bg='#404040', fg='white', 
                        font=('Segoe UI', 9)).pack(pady=2)
                tk.Label(metric_frame, text=value, bg='#404040', fg=color, 
                        font=('Segoe UI', 12, 'bold')).pack(pady=2)
        
        self.metrics_content.grid_columnconfigure(0, weight=1)
        self.metrics_content.grid_columnconfigure(1, weight=1)
        
        # Previsões
        prediction = self.predict_next_month()
        
        # Top 3 categorias que mais gastam
        category_spending = self.df[self.df['Valor'] < 0].groupby('Categoria')['Valor'].sum().abs().sort_values(ascending=False)
        
        predictions_text = f"🔮 Previsão próximo mês: R$ {prediction:,.2f}"
        pred_label = tk.Label(self.predictions_content, text=predictions_text, 
                             bg='#2d2d2d', fg='#ffaa00', font=('Segoe UI', 10, 'bold'))
        pred_label.pack(pady=5)
        
        if len(category_spending) > 0:
            top_text = "🏆 Maiores gastos:\n"
            for i, (cat, value) in enumerate(category_spending.head(3).items()):
                top_text += f"{i+1}. {cat}: R$ {value:,.2f}\n"
            
            top_label = tk.Label(self.predictions_content, text=top_text, 
                               bg='#2d2d2d', fg='#cccccc', font=('Segoe UI', 9))
            top_label.pack(pady=5)
    
    def update_charts(self):
        """Atualizar todos os gráficos"""
        if self.df is None:
            return
        
        self.update_evolution_chart()
        self.update_categories_chart()
        self.update_patterns_chart()
    
    def update_evolution_chart(self):
        """Atualizar gráfico de evolução mensal"""
        self.evolution_ax.clear()
        
        # Agrupar por mês
        monthly_data = self.df.groupby(self.df['Data'].dt.to_period('M')).agg({
            'Valor': lambda x: x[x > 0].sum() - abs(x[x < 0].sum())  # Saldo mensal
        })
        
        if len(monthly_data) > 0:
            months = [str(period) for period in monthly_data.index]
            values = monthly_data['Valor'].values
            
            colors = ['#00ff00' if v >= 0 else '#ff4444' for v in values]
            
            bars = self.evolution_ax.bar(months, values, color=colors, alpha=0.8)
            
            # Linha de tendência
            if len(values) > 1:
                x_numeric = range(len(values))
                z = np.polyfit(x_numeric, values, 1)
                p = np.poly1d(z)
                self.evolution_ax.plot(months, p(x_numeric), "--", color='#ffff00', linewidth=2, alpha=0.8)
            
            self.evolution_ax.set_title('Evolução do Saldo Mensal', color='white', fontsize=14, fontweight='bold')
            self.evolution_ax.set_ylabel('Saldo (R$)', color='white')
            self.evolution_ax.tick_params(colors='white')
            self.evolution_ax.grid(True, alpha=0.3)
            
            # Rotacionar labels do eixo x
            self.evolution_ax.tick_params(axis='x', rotation=45)
        
        self.evolution_canvas.draw()
    
    def update_categories_chart(self):
        """Atualizar gráfico de categorias"""
        self.categories_ax.clear()
        
        # Gastos por categoria (apenas valores negativos)
        category_data = self.df[self.df['Valor'] < 0].groupby('Categoria')['Valor'].sum().abs().sort_values(ascending=False)
        
        if len(category_data) > 0:
            # Cores vibrantes para cada categoria
            colors = plt.cm.Set3(np.linspace(0, 1, len(category_data)))
            
            wedges, texts, autotexts = self.categories_ax.pie(
                category_data.values, 
                labels=category_data.index,
                autopct='%1.1f%%',
                colors=colors,
                startangle=90
            )
            
            # Ajustar cores do texto
            for text in texts:
                text.set_color('white')
            for autotext in autotexts:
                autotext.set_color('black')
                autotext.set_fontweight('bold')
            
            self.categories_ax.set_title('Gastos por Categoria', color='white', fontsize=14, fontweight='bold')
        
        self.categories_canvas.draw()
    
    def update_patterns_chart(self):
        """Atualizar gráfico de padrões (gastos por dia da semana)"""
        self.patterns_ax.clear()
        
        # Gastos por dia da semana
        self.df['DiaSemana'] = self.df['Data'].dt.day_name()
        weekday_spending = self.df[self.df['Valor'] < 0].groupby('DiaSemana')['Valor'].sum().abs()
        
        # Ordenar dias da semana
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        days_pt = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        
        if len(weekday_spending) > 0:
            # Reordenar dados
            ordered_data = []
            ordered_labels = []
            
            for i, day in enumerate(days_order):
                if day in weekday_spending.index:
                    ordered_data.append(weekday_spending[day])
                    ordered_labels.append(days_pt[i])
                else:
                    ordered_data.append(0)
                    ordered_labels.append(days_pt[i])
            
            colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24', '#f0932b', '#eb4d4b', '#6c5ce7']
            
            bars = self.patterns_ax.bar(ordered_labels, ordered_data, color=colors, alpha=0.8)
            
            self.patterns_ax.set_title('Gastos por Dia da Semana', color='white', fontsize=14, fontweight='bold')
            self.patterns_ax.set_ylabel('Gastos (R$)', color='white')
            self.patterns_ax.tick_params(colors='white')
            self.patterns_ax.grid(True, alpha=0.3)
            
            # Rotacionar labels
            self.patterns_ax.tick_params(axis='x', rotation=45)
        
        self.patterns_canvas.draw()


def main():
    """Função principal"""
    root = tk.Tk()
    app = SmartBudgetApp(root)
    
    # Centralizar janela
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    # Ícone da aplicação (se disponível)
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    root.mainloop()


if __name__ == "__main__":
    main()
