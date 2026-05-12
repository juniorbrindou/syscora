import {
  AfterViewInit,
  Component,
  ElementRef,
  OnInit,
  ViewChild,
  inject,
  signal,
} from '@angular/core';
import { DatePipe, DecimalPipe } from '@angular/common';
import { ApiService } from '../../services/api.service';
import { EcritureAnalytique, EvolutionItem, KPIs, RepartitionItem } from '../../models';

declare var echarts: any;

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [DecimalPipe, DatePipe],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class DashboardPage implements OnInit, AfterViewInit {
  private api = inject(ApiService);

  @ViewChild('evolutionChart') evolutionChartEl!: ElementRef;
  @ViewChild('repartitionChart') repartitionChartEl!: ElementRef;

  kpis = signal<KPIs | null>(null);
  recentEcritures = signal<EcritureAnalytique[]>([]);
  evolutionData = signal<EvolutionItem[]>([]);
  repartitionData = signal<RepartitionItem[]>([]);
  loading = signal(true);

  private chartsReady = false;

  ngOnInit(): void {
    this.api.getKPIs().subscribe((k) => this.kpis.set(k));
    this.api.getEcritures(0, 8).subscribe((e) => this.recentEcritures.set(e));
    this.api.getEvolution().subscribe((ev) => {
      this.evolutionData.set(ev);
      if (this.chartsReady) this.renderEvolutionChart(ev);
    });
    this.api.getRepartition().subscribe((r) => {
      this.repartitionData.set(r);
      this.loading.set(false);
      if (this.chartsReady) this.renderRepartitionChart(r);
    });
  }

  ngAfterViewInit(): void {
    this.chartsReady = true;
    const ev = this.evolutionData();
    const rp = this.repartitionData();
    if (ev.length) this.renderEvolutionChart(ev);
    if (rp.length) this.renderRepartitionChart(rp);
  }

  private renderEvolutionChart(data: EvolutionItem[]): void {
    if (!this.evolutionChartEl || typeof echarts === 'undefined') return;
    const chart = echarts.init(this.evolutionChartEl.nativeElement);
    chart.setOption({
      tooltip: {
        trigger: 'axis',
        backgroundColor: '#1f2937',
        borderColor: '#374151',
        textStyle: { color: '#f9fafb', fontSize: 12 },
        formatter: (params: any[]) =>
          params.map((p: any) => `${p.marker} ${p.seriesName}: <b>${p.value.toLocaleString('fr-FR')} €</b>`).join('<br>'),
      },
      legend: {
        data: ['Charges', 'Produits'],
        textStyle: { color: '#6b7280', fontSize: 12 },
        top: 4,
      },
      grid: { left: 12, right: 12, bottom: 8, top: 36, containLabel: true },
      xAxis: {
        type: 'category',
        data: data.map((d) => d.mois),
        axisLine: { lineStyle: { color: '#e5e7eb' } },
        axisTick: { show: false },
        axisLabel: { color: '#9ca3af', fontSize: 11 },
      },
      yAxis: {
        type: 'value',
        axisLabel: { color: '#9ca3af', fontSize: 11, formatter: (v: number) => v >= 1000 ? `${v / 1000}k` : v },
        splitLine: { lineStyle: { color: '#f3f4f6' } },
        axisLine: { show: false },
      },
      series: [
        {
          name: 'Charges',
          type: 'bar',
          data: data.map((d) => d.charges),
          itemStyle: { color: '#6366f1', borderRadius: [4, 4, 0, 0] },
          barMaxWidth: 28,
        },
        {
          name: 'Produits',
          type: 'bar',
          data: data.map((d) => d.produits),
          itemStyle: { color: '#10b981', borderRadius: [4, 4, 0, 0] },
          barMaxWidth: 28,
        },
      ],
    });
    window.addEventListener('resize', () => chart.resize());
  }

  private renderRepartitionChart(data: RepartitionItem[]): void {
    if (!this.repartitionChartEl || typeof echarts === 'undefined') return;
    const colors = ['#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444'];
    const chart = echarts.init(this.repartitionChartEl.nativeElement);
    chart.setOption({
      tooltip: {
        trigger: 'item',
        backgroundColor: '#1f2937',
        borderColor: '#374151',
        textStyle: { color: '#f9fafb', fontSize: 12 },
        formatter: (p: any) => `${p.marker} ${p.name}<br><b>${p.value.toLocaleString('fr-FR')} €</b> (${p.percent}%)`,
      },
      legend: {
        orient: 'vertical',
        right: 0,
        top: 'middle',
        textStyle: { color: '#6b7280', fontSize: 11 },
        itemWidth: 10,
        itemHeight: 10,
      },
      color: colors,
      series: [
        {
          type: 'pie',
          radius: ['45%', '70%'],
          center: ['38%', '50%'],
          avoidLabelOverlap: false,
          label: { show: false },
          emphasis: { label: { show: false } },
          data: data.map((d) => ({ name: d.axe, value: d.montant })),
        },
      ],
    });
    window.addEventListener('resize', () => chart.resize());
  }

  formatMontant(value: number, sens: string): string {
    const sign = sens === 'DEBIT' ? '-' : '+';
    return `${sign}${value.toLocaleString('fr-FR', { minimumFractionDigits: 2 })} €`;
  }
}
