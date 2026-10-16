import { Component, ChangeDetectorRef } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ApiService } from './services/api';

@Component({
  selector: 'app-root',
  imports: [FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {

  message = '';

  messages: {
    text: string;
    sender: 'user' | 'ai';
  }[] = [];

  loading = false;

  constructor(
    private apiService: ApiService,
    private cdr: ChangeDetectorRef
  ) {}

  sendMessage() {

    if (!this.message.trim() || this.loading) {
      return;
    }

    const userMessage = this.message.trim();

    this.messages.push({
      text: userMessage,
      sender: 'user'
    });

    this.message = '';
    this.loading = true;

    this.apiService.sendMessage(userMessage).subscribe({

      next: (result) => {

        console.log('AI response:', result);

        this.messages.push({
          text: result.response,
          sender: 'ai'
        });

        this.loading = false;

        this.cdr.detectChanges();

      },

      error: (error) => {

        console.error('API error:', error);

        this.messages.push({
          text: 'Sorry, I could not connect to the AI server.',
          sender: 'ai'
        });

        this.loading = false;

        this.cdr.detectChanges();

      }

    });

  }

  useSuggestion(question: string) {

    this.message = question;

    this.sendMessage();

  }

}