import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CorrelacaoFornecedorDeputadoComponent } from './correlacao-fornecedor-deputado.component';

describe('CorrelacaoFornecedorDeputadoComponent', () => {
  let component: CorrelacaoFornecedorDeputadoComponent;
  let fixture: ComponentFixture<CorrelacaoFornecedorDeputadoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CorrelacaoFornecedorDeputadoComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CorrelacaoFornecedorDeputadoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
