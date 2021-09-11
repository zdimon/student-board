import React from 'react';
// import ReactDOM from 'react-dom';
import { render } from 'react-dom';
import StudentMenu from './components/menu/StudentMenu';

const smenuEl = document.getElementById('js-student-menu');
console.log(smenuEl);
if (smenuEl) render(<StudentMenu selector="JSpopJournalsItems" />, smenuEl);
