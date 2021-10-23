import React from 'react';
// import ReactDOM from 'react-dom';
import { render } from 'react-dom';
import StudentMenu from './components/menu/StudentMenu';
import KursakMenu from './components/menu/KursakMenu';

const smenuEl = document.getElementById('js-student-menu');
if (smenuEl) render(<StudentMenu selector="JSpopJournalsItems" />, smenuEl);

const kmenuEl = document.getElementById('js-kursak-menu');
if (kmenuEl) render(<KursakMenu selector="JSpopJournalsItems" />, kmenuEl);
