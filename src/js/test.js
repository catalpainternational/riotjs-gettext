import Catalog from './catalog.js';
var assert = require('assert');

const tet = new Catalog({
  'Activity': 'Actividade',
  'Project': 'Projetu',
  'verb\x04may': 'bele',
  'month\x04may': 'maiu',
  'animal\x04Elephant': 'Amimal abu-abu neebe boot',
  'There is one activity': ['Iha atividade ida', 'Iha atividade barak'],
  'foo\x04There is one activity': ['Iha foo ida', 'Iha foo barak'],
  'bar\x04There is one activity': ['Iha bar ida', 'Iha bar barak'],
  'There is %(total)s object. Remaining: %(count)s': ['Iha %(total)s objetu. Restu mak: %(count)s', 'Iha %(total)s objetu sira. Restu mak: %(count)s'],
  'I caught %s pocket monster!. Remaining: %s': ["Hau kaer %s pokemon deit!. Sei livre: %s", "Hau kaer %s pokemon! Sei livre: %s"]
})

describe("Tetun translations", function(){
  it('should translate Activity to Actividade', () => {
    assert.equal( tet.translate('', 'Activity'), 'Actividade');
  }),

  it('should translate contextual markers when present', () => {
    assert.equal(tet.translate('verb', 'may'), 'bele');
    assert.equal( tet.translate('month', 'may'), 'maiu');
  })

  it('should translate interpolated positional markers when present', () => {

    assert.equal(tet.translate('', 'There is %(total)s object. Remaining: %(count)s', 'There are %(total)s objects. Remaining: %(count)s', 1, '', {'total': 1, 'count': 10}), 'Iha 1 objetu. Restu mak: 10');
    assert.equal(tet.translate('', 'There is %(total)s object. Remaining: %(count)s', 'There are %(total)s objects. Remaining: %(count)s', 5, '', {'total': 5, 'count': 10}), 'Iha 5 objetu sira. Restu mak: 10');
  })
  it('Should not require a plural for translation', () => {
    assert.equal(tet.translate('', 'There is %(total)s object. Remaining: %(count)s', '', 5, '', {'total': 5, 'count': 10}), 'Iha 5 objetu sira. Restu mak: 10');
  })

})
