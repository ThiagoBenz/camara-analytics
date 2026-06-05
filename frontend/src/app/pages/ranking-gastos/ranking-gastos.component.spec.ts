import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RankingGastosComponent } from './ranking-gastos.component';

describe('RankingGastosComponent', () => {
  let component: RankingGastosComponent;
  let fixture: ComponentFixture<RankingGastosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RankingGastosComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RankingGastosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
