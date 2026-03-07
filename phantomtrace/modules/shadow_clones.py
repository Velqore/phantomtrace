#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
Shadow Clones - Generate fake files and activity to create noise

Creates decoy documents, browser history, file access patterns etc.
Makes forensic analysis harder by adding realistic-looking fake data.
"""

import os
import secrets
import json
from datetime import datetime, timedelta
from pathlib import Path
import string


class ShadowClone:
    """Generate fake files and browsing history to muddy the waters."""
    
    # Common document types
    DOCUMENT_TEMPLATES = [
        "meeting_notes", "project_plan", "budget", "report",
        "memo", "proposal", "invoice", "contract"
    ]
    
    WEBSITES = [
        "news", "social", "shopping", "education",
        "entertainment", "work", "research", "finance"
    ]
    
    FILE_TYPES = {
        'documents': ['.txt', '.docx', '.pdf', '.xlsx'],
        'images': ['.jpg', '.png', '.gif'],
        'code': ['.py', '.js', '.java', '.cpp'],
        'data': ['.csv', '.json', '.xml', '.db']
    }
    
    def __init__(self, output_dir="./decoys"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.generated = []
    
    def create_believable_decoys(self, activity_type="mixed", count=50, time_range_days=90):
        """Create fake files/history entries that look real."""
        created_files = []
        
        for _ in range(count):
            if activity_type == "browsing" or (activity_type == "mixed" and secrets.randbits(1)):
                # Create browser history entry
                entry = self._generate_browser_history_entry(time_range_days)
                created_files.append(entry)
            else:
                # Create document decoy
                doc = self._generate_document_decoy(time_range_days)
                created_files.append(doc)
        
        self.generated.extend(created_files)
        return created_files
    
    def _generate_browser_history_entry(self, time_range_days: int) -> str:
        """Generate realistic browser history entry."""
        # Generate random timestamp within range
        timestamp = datetime.now() - timedelta(
            days=secrets.randbelow(time_range_days),
            hours=secrets.randbelow(24),
            minutes=secrets.randbelow(60)
        )
        
        # Generate realistic URL
        url = self._generate_realistic_url()
        
        # Generate page title
        title = self._generate_page_title(url)
        
        # Create history entry
        entry = {
            'timestamp': timestamp.isoformat(),
            'url': url,
            'title': title,
            'visit_count': secrets.randbelow(5) + 1,
            'typed_count': secrets.randbelow(2)
        }
        
        # Save to file
        filename = f"history_{timestamp.strftime('%Y%m%d_%H%M%S')}_{secrets.token_hex(4)}.json"
        filepath = self.output_dir / "browsing" / filename
        filepath.parent.mkdir(exist_ok=True, parents=True)
        
        with open(filepath, 'w') as f:
            json.dump(entry, f, indent=2)
        
        return str(filepath)
    
    def _generate_realistic_url(self):
        # Pick random domain and path
        domains = [
            "news.example.com", "shop.example.net", "learn.example.edu",
            "social.example.com", "work.example.com", "tech.example.org"
        ]
        
        paths = [
            "/articles/", "/products/", "/courses/", "/posts/",
            "/documents/", "/resources/", "/blog/", "/news/"
        ]
        
        domain = secrets.choice(domains)
        path = secrets.choice(paths)
        slug = ''.join(secrets.choice(string.ascii_lowercase) for _ in range(10))
        
        return f"https://{domain}{path}{slug}"
    
    def _generate_page_title(self, url):
        if 'news' in url:
            return f"Breaking: {self._random_words(3, 6)}"
        elif 'shop' in url:
            return f"{self._random_words(2, 4)} - Buy Online"
        elif 'learn' in url:
            return f"Course: {self._random_words(3, 5)}"
        elif 'social' in url:
            return f"{self._random_words(1, 2)}'s Post"
        else:
            return self._random_words(3, 7)
    
    def _generate_document_decoy(self, time_range_days):
        # Pick a document type and generate content
        doc_type = secrets.choice(self.DOCUMENT_TEMPLATES)
        content = self._generate_document_content(doc_type)
        
        # Generate timestamp
        timestamp = datetime.now() - timedelta(
            days=secrets.randbelow(time_range_days),
            hours=secrets.randbelow(24)
        )
        
        # Choose file extension
        category = secrets.choice(list(self.FILE_TYPES.keys()))
        extension = secrets.choice(self.FILE_TYPES[category])
        
        # Create filename
        filename = f"{doc_type}_{timestamp.strftime('%Y%m%d')}_{secrets.token_hex(4)}{extension}"
        filepath = self.output_dir / "documents" / filename
        filepath.parent.mkdir(exist_ok=True, parents=True)
        
        # Write content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Set realistic timestamp
        atime = mtime = timestamp.timestamp()
        os.utime(filepath, (atime, mtime))
        
        return str(filepath)
    
    def _generate_document_content(self, doc_type: str) -> str:
        """Generate realistic document content."""
        if doc_type == "meeting_notes":
            return self._generate_meeting_notes()
        elif doc_type == "project_plan":
            return self._generate_project_plan()
        elif doc_type == "budget":
            return self._generate_budget()
        else:
            return self._generate_generic_document()
    
    def _generate_meeting_notes(self) -> str:
        """Generate realistic meeting notes."""
        date = (datetime.now() - timedelta(days=secrets.randbelow(30))).strftime('%Y-%m-%d')
        
        content = f"""Meeting Notes - {date}
        
Attendees:
{self._random_names(3, 6)}

Agenda:
1. {self._random_words(3, 6)}
2. {self._random_words(4, 7)}
3. {self._random_words(3, 5)}

Discussion:
{self._random_paragraphs(2, 4)}

Action Items:
- {self._random_words(4, 8)}
- {self._random_words(5, 9)}
- {self._random_words(3, 7)}

Next Meeting: {(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')}
"""
        return content
    
    def _generate_project_plan(self) -> str:
        """Generate realistic project plan."""
        project_name = self._random_words(2, 4)
        
        content = f"""Project Plan: {project_name}

Overview:
{self._random_paragraphs(1, 2)}

Objectives:
1. {self._random_words(5, 10)}
2. {self._random_words(5, 10)}
3. {self._random_words(5, 10)}

Timeline:
Phase 1: {self._random_words(3, 5)} (Weeks 1-2)
Phase 2: {self._random_words(3, 5)} (Weeks 3-4)
Phase 3: {self._random_words(3, 5)} (Weeks 5-6)

Resources:
{self._random_paragraphs(1, 2)}

Risks:
- {self._random_words(5, 10)}
- {self._random_words(5, 10)}
"""
        return content
    
    def _generate_budget(self) -> str:
        """Generate realistic budget."""
        content = f"""Budget Report

Generated: {datetime.now().strftime('%Y-%m-%d')}

Category, Amount, Notes
"""
        for _ in range(5, 10):
            category = self._random_words(1, 2)
            amount = secrets.randbelow(10000) + 100
            notes = self._random_words(3, 6)
            content += f"{category}, ${amount:,.2f}, {notes}\n"
        
        return content
    
    def _generate_generic_document(self) -> str:
        """Generate generic document content."""
        return f"""Document: {self._random_words(2, 4)}

Date: {datetime.now().strftime('%Y-%m-%d')}

{self._random_paragraphs(3, 6)}

Summary:
{self._random_paragraphs(1, 2)}
"""
    
    def _random_words(self, min_count: int, max_count: int) -> str:
        """Generate random words."""
        word_list = [
            "project", "system", "process", "data", "management", "analysis",
            "report", "update", "review", "strategy", "implementation", "development",
            "research", "evaluation", "planning", "execution", "monitoring", "optimization"
        ]
        
        count = secrets.randbelow(max_count - min_count + 1) + min_count
        words = [secrets.choice(word_list) for _ in range(count)]
        return ' '.join(words).capitalize()
    
    def _random_paragraphs(self, min_count: int, max_count: int) -> str:
        """Generate random paragraphs."""
        count = secrets.randbelow(max_count - min_count + 1) + min_count
        paragraphs = []
        
        for _ in range(count):
            sentences = secrets.randbelow(4) + 2
            paragraph = []
            for _ in range(sentences):
                sentence = self._random_words(8, 15) + '.'
                paragraph.append(sentence)
            paragraphs.append(' '.join(paragraph))
        
        return '\n\n'.join(paragraphs)
    
    def _random_names(self, min_count: int, max_count: int) -> str:
        """Generate random names."""
        first_names = ["John", "Jane", "Michael", "Sarah", "David", "Emily", "Robert", "Lisa"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
        
        count = secrets.randbelow(max_count - min_count + 1) + min_count
        names = []
        for _ in range(count):
            first = secrets.choice(first_names)
            last = secrets.choice(last_names)
            names.append(f"- {first} {last}")
        
        return '\n'.join(names)
    
    def create_file_access_trail(
        self,
        directory: str,
        num_accesses: int = 100,
        time_range_days: int = 30
    ) -> int:
        """
        Create realistic file access pattern by touching files.
        
        Args:
            directory: Directory to create access pattern in
            num_accesses: Number of file accesses to simulate
            time_range_days: Spread accesses across this many days
        
        Returns:
            Number of files accessed
        """
        dir_path = Path(directory)
        files = [f for f in dir_path.rglob('*') if f.is_file()]
        
        if not files:
            return 0
        
        accessed_count = 0
        for _ in range(num_accesses):
            # Pick random file
            filepath = secrets.choice(files)
            
            # Generate random access time
            access_time = datetime.now() - timedelta(
                days=secrets.randbelow(time_range_days),
                hours=secrets.randbelow(24),
                minutes=secrets.randbelow(60)
            )
            
            # Touch file with new access time
            stat = filepath.stat()
            os.utime(filepath, (access_time.timestamp(), stat.st_mtime))
            accessed_count += 1
        
        return accessed_count
    
    def get_generated_decoys(self):
        return self.generated.copy()
