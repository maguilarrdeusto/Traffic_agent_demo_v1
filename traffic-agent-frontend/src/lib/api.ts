/**
 * Cliente API para comunicarse con el backend del agente de tráfico.
 */

// URL base del backend
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

/**
 * Interfaz para la solicitud de chat
 */
export interface ChatRequest {
  message: string;
  session_id?: string;
}

/**
 * Interfaz para la respuesta de chat
 */
export interface ChatResponse {
  response: string;
  session_id: string;
}

/**
 * Interfaz para un mensaje de conversación
 */
export interface ChatMessage {
  id: number;
  user_message: string;
  agent_response: string;
  optimizer_type: string | null;
  weights: Record<string, number>;
  created_at: string;
}

/**
 * Interfaz para el historial de conversación
 */
export interface ChatHistory {
  session_id: string;
  history: ChatMessage[];
}

/**
 * Cliente API para el agente de tráfico
 */
export const api = {
  /**
   * Envía un mensaje al agente de tráfico
   * 
   * @param message Mensaje del usuario
   * @param session_id ID de sesión opcional
   * @returns Respuesta del agente
   */
  async sendMessage(message: string, session_id?: string): Promise<ChatResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          session_id,
        }),
      });

      if (!response.ok) {
        throw new Error(`Error en la solicitud: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error al enviar mensaje:', error);
      throw error;
    }
  },

  /**
   * Obtiene el historial de conversación para una sesión
   * 
   * @param session_id ID de la sesión
   * @returns Historial de conversación
   */
  async getHistory(session_id: string): Promise<ChatHistory> {
    try {
      const response = await fetch(`${API_BASE_URL}/history/${session_id}`);

      if (!response.ok) {
        throw new Error(`Error al obtener historial: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error al obtener historial:', error);
      throw error;
    }
  },

  /**
   * Verifica el estado del backend y las APIs externas
   * 
   * @returns Estado del sistema
   */
  async checkHealth(): Promise<Record<string, any>> {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);

      if (!response.ok) {
        throw new Error(`Error al verificar estado: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error al verificar estado:', error);
      throw error;
    }
  },
};
