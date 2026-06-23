import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViesPoliticoComponent } from './vies-politico.component';

describe('ViesPoliticoComponent', () => {
  let component: ViesPoliticoComponent;
  let fixture: ComponentFixture<ViesPoliticoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViesPoliticoComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViesPoliticoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
