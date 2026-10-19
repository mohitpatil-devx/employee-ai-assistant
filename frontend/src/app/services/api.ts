import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

interface ChatResponse {
  response: string;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private apiUrl = 'https://employee-ai-assistant-je4p.onrender.com/api';

  constructor(private http: HttpClient) {}

  sendMessage(message: string): Observable<ChatResponse> {
    return this.http.post<ChatResponse>(
      `${this.apiUrl}/chat`,
      { message }
    );
  }
}