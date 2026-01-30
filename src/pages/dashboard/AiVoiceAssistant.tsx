import { useEffect, useRef, useState } from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Mic, MicOff, Volume2, Bot, User } from 'lucide-react';

interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
}

export default function AIVoiceAssistant() {
  const [listening, setListening] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    // Browser Speech Recognition
    const SpeechRecognition =
      (window as any).SpeechRecognition ||
      (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) return;

    const recognition = new SpeechRecognition();
    recognition.lang = 'en-IN';
    recognition.interimResults = false;
    recognition.continuous = false;

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;

      const userMessage: Message = {
        id: Date.now(),
        role: 'user',
        content: transcript,
      };

      setMessages((prev) => [...prev, userMessage]);

      // TODO: Send transcript to AI model here
      const aiPlaceholder: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        content: '🤖 AI response will appear here (model not integrated yet).',
      };

      setMessages((prev) => [...prev, aiPlaceholder]);

      // TODO: Text-to-speech for AI response
      speak(aiPlaceholder.content);
    };

    recognition.onend = () => {
      setListening(false);
    };

    recognitionRef.current = recognition;
  }, []);

  const startListening = () => {
    if (!recognitionRef.current) return;
    setListening(true);
    recognitionRef.current.start();
  };

  const stopListening = () => {
    recognitionRef.current?.stop();
    setListening(false);
  };

  const speak = (text: string) => {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-IN';
    window.speechSynthesis.speak(utterance);
  };

  return (
    <DashboardLayout>
      <div className="p-6 lg:p-8 space-y-6 max-w-4xl mx-auto">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Bot className="h-5 w-5 text-primary" />
              AI Voice Assistant
            </CardTitle>
            <Badge variant="secondary">Beta</Badge>
          </CardHeader>

          <CardContent className="space-y-6">
            {/* Chat Area */}
            <div className="border rounded-lg p-4 h-[350px] overflow-y-auto space-y-4 bg-muted/30">
              {messages.length === 0 && (
                <p className="text-sm text-muted-foreground text-center">
                  Start speaking to interact with the AI assistant 🎤
                </p>
              )}

              {messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`flex gap-2 ${
                    msg.role === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  <div
                    className={`max-w-[75%] rounded-lg px-4 py-2 text-sm ${
                      msg.role === 'user'
                        ? 'bg-primary text-primary-foreground'
                        : 'bg-background border'
                    }`}
                  >
                    <div className="flex items-center gap-2 mb-1">
                      {msg.role === 'user' ? (
                        <User className="h-3 w-3" />
                      ) : (
                        <Bot className="h-3 w-3 text-primary" />
                      )}
                      <span className="text-xs opacity-70">
                        {msg.role === 'user' ? 'You' : 'Assistant'}
                      </span>
                    </div>
                    {msg.content}
                  </div>
                </div>
              ))}
            </div>

            {/* Controls */}
            <div className="flex items-center justify-center gap-4">
              {!listening ? (
                <Button onClick={startListening} className="gap-2">
                  <Mic className="h-4 w-4" />
                  Start Listening
                </Button>
              ) : (
                <Button variant="destructive" onClick={stopListening} className="gap-2">
                  <MicOff className="h-4 w-4" />
                  Stop
                </Button>
              )}

              <Button
                variant="outline"
                onClick={() => speak('This is a sample AI voice output')}
                className="gap-2"
              >
                <Volume2 className="h-4 w-4" />
                Test Voice Output
              </Button>
            </div>

            {/* Placeholder for AI integration */}
            {/* <div className="text-xs text-muted-foreground border-t pt-4">
              🔧 <strong>AI Integration Placeholder:</strong>  
              Connect your LLM / Supabase Edge Function / API here.
            </div> */}
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}